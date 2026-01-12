# 3rd party
from coincidence.regressions import AdvancedFileRegressionFixture
from domdf_python_tools.paths import PathPlus

# this package
from formate import yapf_hook


def test_nested_call(advanced_file_regression: AdvancedFileRegressionFixture):
	src = """
a = cls(**dict(map(
		lambda f: (f[0].name, curried.get_in(f[1], d, f[0].default)),
		from_fields,
		)⸴ )⸴ )
""".replace('⸴', ',')

	advanced_file_regression.check(yapf_hook(src))


def test_nested_array(advanced_file_regression: AdvancedFileRegressionFixture):
	src = """
def foo():
	example = {
			"table": {"nested_table": [
					{"array_options": [1, 2, 3]},
					{"another_array": [1, 2]},
					{'c': 3},
					]⸴ },
			}
""".replace('⸴', ',')

	advanced_file_regression.check(
			yapf_hook(src, yapf_style=PathPlus(__file__).parent.parent.joinpath(".style.yapf").as_posix()),
			)


def test_tuple():
	src = 'top_tmp["normalized"] = top_tmp.apply(normalize, args=(max(top_tmp["intensity"]), ), axis=1)\n'
	assert yapf_hook(src, yapf_style=PathPlus(__file__).parent.parent.joinpath(".style.yapf").as_posix()) == src
