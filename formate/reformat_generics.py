#!/usr/bin/env python3
#
#  reformat_generics.py
"""
Formats generics (``List[...]``, ``Union[...]`` etc.) at the module and class level.

Example output, with a line length of ``100``:

.. code-block:: python

	ParamsMappingValueType = Union[str, bytes, int, float, Iterable[Union[str, bytes, int, float]]]
	Data = Union[None, str, bytes, MutableMapping[str, Any], Iterable[Tuple[str, Optional[str]]], IO]
	ParamsType = Union[
		Mapping[Union[str, bytes, int, float], ParamsMappingValueType],
		Union[str, bytes],
		Tuple[Union[str, bytes, int, float], ParamsMappingValueType],
		None
		]
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import ast
import sys
import typing
from collections.abc import Collection
from io import StringIO
from textwrap import indent as indent_string

# 3rd party
import astatine
import asttokens
from domdf_python_tools.stringlist import DelimitedList, StringList
from domdf_python_tools.words import TAB

__all__ = ("reformat_generics", "Generic", "List")

collection_types = {"Union", "List", "Tuple", "Set", "Dict", "Callable", "Optional", "Literal"}

subclasses = [Collection]
# pylint: disable=loop-global-usage
while subclasses:
	subclass = subclasses.pop(0)
	if subclass.__module__ == "collections.abc":
		collection_types.add(subclass.__name__)
		subclasses.extend(subclass.__subclasses__())
		# pylint: enable=loop-global-usage


def get_slice_value(ast_slice):  # py36: ast.Index  # py39: ast.Tuple  # noqa: MAN001,MAN002
	"""
	Return the value of the slice in a Python version-independent way.

	:param ast_slice:
	"""

	if sys.version_info < (3, 9):  # pragma: no cover (py39+)
		return ast_slice.value
	else:
		return ast_slice  # pragma: no cover (<py39)


class Generic:
	"""
	Represents a :class:`typing.Generic`, :py:obj:`typing.Union`, :py:obj:`typing.Callable` etc.

	:param name: The name of the Generic
	:param elements: The ``__class_getitem__`` elements of the Generic.
	"""

	def __init__(self, name: str, elements: typing.Sequence[typing.Union[str, "Generic", "List"]]):
		self.name = str(name)
		self.elements: DelimitedList[typing.Union[str, Generic, List]] = DelimitedList(elements)

	def __repr__(self) -> str:
		return f"{self.name}[{self.elements:, }]"

	def format(self, line_offset: int = 0) -> str:  # noqa: A003  # pylint: disable=redefined-builtin
		"""
		Formats the :class:`~.Generic`.

		:param line_offset:
		"""

		if line_offset + len(repr(self)) > 110:
			# Line too long as is
			elements: DelimitedList[str] = DelimitedList()
			offset_plus_4 = line_offset + 4
			for element in self.elements:
				if isinstance(element, Generic):
					elements.append(indent_string(element.format(offset_plus_4), '\t'))
				else:
					elements.append(indent_string(str(element), '\t'))
			return f"{self.name}[\n{elements:,\n}\n	]"
		else:
			return repr(self)


class List:
	"""
	Represents a list of elements, most often used within a :py:obj:`typing.Callable`.

	:param elements:
	"""

	def __init__(self, elements: typing.Sequence[typing.Union[str, Generic, "List"]]):
		self.elements = DelimitedList(elements)

	def __repr__(self) -> str:
		return f"[{self.elements:, }]"


class Visitor(ast.NodeVisitor):
	in_class = False

	def __init__(self):
		self.unions: typing.List[typing.Tuple[ast.Subscript, Generic, bool]] = []

	def visit_Subscript(self, node: ast.Subscript) -> None:
		if isinstance(node.value, ast.Name) and node.value.id in collection_types:
			union = Generic(node.value.id, UnionVisitor().visit(get_slice_value(node.slice)))
			self.unions.append((node, union, self.in_class))
			return

		elif isinstance(node.value, ast.Attribute):
			if isinstance(node.value.value, ast.Name) and node.value.value.id in {"typing", "typing_extensions"}:
				if node.value.attr in collection_types:
					union = Generic(
							'.'.join([node.value.value.id, node.value.attr]),
							UnionVisitor().visit(get_slice_value(node.slice)),
							)
					self.unions.append((node, union, self.in_class))
					return

		self.generic_visit(node)

	def visit(self, node: ast.AST) -> typing.List[typing.Tuple[ast.Subscript, Generic, bool]]:
		super().visit(node)
		return self.unions

	def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
		return None

	def visit_ClassDef(self, node: ast.ClassDef) -> None:
		self.unions.extend(ClassVisitor().visit(node))

	def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
		return None


class ClassVisitor(Visitor):
	in_class = True

	def visit_ClassDef(self, node: ast.ClassDef) -> None:
		self.generic_visit(node)


class UnionVisitor(ast.NodeVisitor):

	def __init__(self):
		super().__init__()
		self.structure: typing.List[typing.Union[str, Generic, List]] = []

	def generic_visit(self, node: ast.AST) -> None:
		super().generic_visit(node)

	def visit_Name(self, node: ast.Name) -> None:
		self.structure.append(f"{node.id}")

	def visit_Attribute(self, node: ast.Attribute) -> None:
		parts: DelimitedList[str] = DelimitedList()
		value: typing.Union[ast.Name, ast.expr] = node.value

		NameNode, AttributeNode = ast.Name, ast.Attribute

		while True:
			if isinstance(value, NameNode):
				parts.append(value.id)
				break
			elif isinstance(value, AttributeNode):
				parts.append(value.value.id)  # type: ignore[attr-defined]
				value = value.attr  # type: ignore[assignment]
			elif isinstance(value, str):
				parts.append(value)
				break
			else:
				raise NotImplementedError(f"Unsupported value type {type(value)}")

		self.structure.append(f"{parts:.}.{node.attr}")

	def visit_Subscript(self, node: ast.Subscript) -> None:
		union = Generic(
				'.'.join(astatine.get_attribute_name(node.value)),
				UnionVisitor().visit(get_slice_value(node.slice)),
				)
		self.structure.append(union)

	def visit_List(self, node: ast.List) -> None:
		elements = []
		for child in node.elts:
			elements.extend(UnionVisitor().visit(child))
		self.structure.append(List(elements))

	def visit_Load(self, node: ast.Load) -> None:
		return None

	def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
		return None

	def visit_ClassDef(self, node: ast.ClassDef) -> None:
		self.generic_visit(node)

	def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
		return None

	if sys.version_info[:2] < (3, 8):  # pragma: no cover (py38+)

		def visit_NameConstant(self, node: ast.NameConstant) -> None:
			self.structure.append(node.value)

		def visit_Str(self, node: ast.Str) -> None:
			self.structure.append(f'"{node.s}"')

		def visit_Ellipsis(self, node: ast.Ellipsis) -> None:
			self.structure.append("...")

	else:  # pragma: no cover (<py38)

		def visit_Constant(self, node: ast.Constant) -> None:
			if isinstance(node.value, str):
				self.structure.append(f'"{node.value}"')
			elif node.value is Ellipsis:
				self.structure.append("...")
			elif node.value is None or isinstance(node.value, bool):
				self.structure.append(str(node.value))
			else:
				print(node, node.value)
				self.generic_visit(node)

	def visit(self, node: ast.AST) -> typing.List[typing.Union[str, Generic, List]]:
		super().visit(node)
		return self.structure


def reformat_generics(
		source: str,
		formate_global_config: typing.Optional[typing.Mapping] = None,
		**kwargs,
		) -> str:
	r"""
	Reformats generics (:class:`typing.Generic`, :py:obj:`typing.Union`, :py:obj:`typing.Callable` etc.)
	in the given source, and returns the reformatted source.

	:param source: The source to reformat.
	:param formate_global_config: The global configuration dictionary. Optional.
	:param \*\*kwargs:

	:returns: The reformatted source.

	.. raw:: latex

		\clearpage
	"""  # noqa: D400

	offset = 0
	buf = StringIO()
	visitor = Visitor()
	atok = asttokens.ASTTokens(source, parse=True)
	tree = atok.tree
	assert tree is not None

	indent = (formate_global_config or {}).get("indent", kwargs.get("indent", TAB))

	try:
		for union_node, union_obj, in_class in visitor.visit(tree):
			text_range = atok.get_text_range(union_node)
			buf.write(source[offset:text_range[0]])

			reversed_line = source[offset:text_range[0]][::-1]

			if '\n' in reversed_line:
				line_offset = reversed_line.index('\n')
			else:
				line_offset = 0

			formatted_obj = StringList(union_obj.format(line_offset))

			if in_class and len(formatted_obj) > 1:
				buf.write(formatted_obj[0])
				buf.write('\n')
				buf.write(indent_string(str(StringList(formatted_obj[1:])), indent))
			elif in_class:
				buf.write(formatted_obj[0])
			else:
				buf.write(str(formatted_obj))

			offset = text_range[1]

		buf.write(source[offset:])

		if indent != TAB:
			return buf.getvalue().expandtabs(len(indent))
		else:
			return buf.getvalue()

	except NotImplementedError as e:  # pragma: no cover
		print(f"An error occurred: {e}")
		return source
