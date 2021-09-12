"""Build static HTML site from directory of HTML templates and plain files."""
import sys
import pathlib
import shutil
import json
from json.decoder import JSONDecodeError
import jinja2
import click


@click.command()
@click.option('-o', "--output", type=click.Path(), help="Output directory.")
@click.option('-v', "--verbose", is_flag=True, help="Print more output.")
@click.argument("input_dir", type=click.Path())
def main(input_dir, output, verbose):
    """Templated static website generator."""
    if not pathlib.Path(str(input_dir)).exists():
        print("Input Directory {} doesn't exist.".format(str(input_dir)))
        sys.exit(1)

    output_dir = pathlib.Path('/').joinpath(
        str(input_dir), "html")\
        if not output\
        else pathlib.Path(str(output))
    output_dir = str(output_dir).lstrip('/')
    if pathlib.Path(output_dir).exists():
        print("Ouput Directory {} already exists.".format(str(output_dir)))
        sys.exit(1)
    output_dir = pathlib.Path(str(output_dir))
    output_dir.mkdir(exist_ok=True, parents=True)

    static_dir = str(
        pathlib.Path('/').joinpath(str(input_dir), "static")).lstrip('/')
    if pathlib.Path(static_dir).exists():
        shutil.copytree(static_dir, output_dir, dirs_exist_ok=True)
        if verbose:
            click.echo("Copied {} -> {}".format(static_dir, output_dir))

    template_dir = str(
        pathlib.Path('/').joinpath(str(input_dir), "templates")).lstrip('/')
    jsonhelper(input_dir, template_dir, output_dir, verbose)


def jsonhelper(input_dir, template_dir, output_dir, verbose):
    """Json Helper Function."""
    for file in pathlib.Path(input_dir).glob('*'):
        if str(file.parts[-1]) == "config.json":
            with open(str(file), 'r') as json_file:
                try:
                    json_object = json.load(json_file)
                except JSONDecodeError as error:
                    print("Json error is raised when loading json file: {}."
                          .format(error))
                try:
                    template_env = jinja2.Environment(
                        loader=jinja2.FileSystemLoader(str(template_dir)),
                        autoescape=jinja2.select_autoescape(['html', 'xml']),
                    )
                except jinja2.TemplateError as error:
                    print("Jinja error or templates directory(file)-not-found \
                          error is raised when loading Environment: {}."
                          .format(error))
                    sys.exit(1)
                for json_dict_1 in json_object:
                    try:
                        template_html = template_env.get_template(
                                        json_dict_1["template"])
                    except jinja2.TemplateSyntaxError as error:
                        print("Jinja error or index.html file-not-found error \
                              is raised when get_template: {}.".format(error))
                        sys.exit(1)
                    html_output_dir = str(
                        pathlib.Path('/')
                        .joinpath(
                            str(output_dir),
                            str(json_dict_1["url"].strip('/')))).lstrip('/')
                    html_output_dir = pathlib.Path(str(html_output_dir))
                    html_output_dir.mkdir(exist_ok=True, parents=True)
                    html_output_path = str(
                        pathlib.Path('/')
                        .joinpath(html_output_dir, "index.html")).lstrip('/')
                    with open(html_output_path, 'w') as final_html:
                        html_content = template_html.render(
                                       json_dict_1["context"])
                        final_html.write(html_content)
                    if verbose:
                        click.echo("Rendered {} -> {}".format(
                                   json_dict_1["template"], html_output_path))
            break


if __name__ == "__main__":
    main()
