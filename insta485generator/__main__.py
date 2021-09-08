"""Build static HTML site from directory of HTML templates and plain files."""
import click
import pathlib
import jinja2
import shutil

@click.command()
@click.option('-o', "--output", type=click.Path(), help="Output directory.")
@click.option('-v', "--verbose", help="Print more output.")
@click.argument("INPUT_DIR", type=click.Path())

def main():
    """Top level command line interface."""
    if not pathlib.Path(str(INPUT_DIR)).exists():
        print("Input Directory {} doesn't exist.".format(str(INPUT_DIR)))
        exit(1)

    output_path = None
    if not output:
        output_path = pathlib.Path('/').joinpath(str(INPUT_DIR), 'html')
    else:
        output_path = output
    if pathlib.Path(output_path).exists():
        print("Output Directory {} already exists.".format(str(output_path)))
        exit(1)

    template_dir = pathlib.Path('/').joinpath(str(INPUT_DIR), 'templates')
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(template_dir)),
        audoescape=jinja2.select_autoescape(['html', 'xml']),
    )
    html_file = (pathlib.PurePath(template_dir).parts)[-1]
    template_template = template_env.get_template(html_file)
    
    shutil.copy(template_template, output_path)

    static_path = pathlib.Path('/').joinpath(output_path, 'static')
    if pathlib.Path(static_path).exists():
        for file in path.rglob('*'):
            src_path = pathlib.Path('/').joinpath(static_path, file)
            shutil.copy(src_path, output_path)
    
    render_output_path = pathlib.Path('/').joinpath(str(output_path), html_file)
    if verbose:
        print("Rendered {} -> {}".format(str(html_file), str(render_output_path)))


    if not pathlib.Path(str(INPUT_DIR)).exists():
        print("Input Directory {} doesn't exist.".format(str(INPUT_DIR)))
        exit(1)

    output_dir = None
    if not output:
        output_dir = pathlib.Path('/').joinpath(str(INPUT_DIR), "html")
    else:
        output_dir = pathlib.Path('/').joinpath(str(INPUT_DIR), str(output))
    if pathlib.Path(output_dir).exists():
        print("Ouput Directory {} already exists.".format(str(output_dir)))
        exit(1)

    static_dir = pathlib.Path('/').joinpath(str(output_dir), "static")
    if static_dir.exists():
        for file in static_dir.rglob('*'):
            src_dir = pathlib.Path('/').joinpath(str(static_dir), str(file))
            shutil.copy(src_dir, output_dir)

    for file in INPUT_DIR.rglob('*'):
        if str(file) == "config.json":
            with open(str(file), 'r') as json_file:
                json_object = json.load(json_file)
                for json_dict_1 in json_object:
                    for item_1 in json_dict_1:
                        template_dir = pathlib.Path('/').joinpath(str(INPUT_DIR), "templates")
                        try:
                            template_env = jinj2.Environment
            break

if __name__ == "__main__":
    main()
