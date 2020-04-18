#------------------------------------------------------------------------------#
#                     Author     : Nicklas Sindlev Andersen                    #
#------------------------------------------------------------------------------#
#
#------------------------------------------------------------------------------#
#               Import packages from the python standard library               #
#------------------------------------------------------------------------------#
import os
#------------------------------------------------------------------------------#
#                           Import local libraries/code                        #
#------------------------------------------------------------------------------#
from HashTable import HashTable
#------------------------------------------------------------------------------#
#                           Import thrid party packages                        #
#------------------------------------------------------------------------------#
import jinja2


#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
class HashTableRenderer(HashTable):
    """
    A simple class for rendering a set of pre-specified jinja templates (located
    in the ./base directory) to a set of Tikz illustrations.

    The jinja templates use the insertion/search events generated within the 
    "HashTable" class.

    The Tikz illustrations are compiled into a final "main.tex" document, which
    can be converted into e.g. a LaTeX beamer presentation. 
    """

    def __init__(self, size, hash_function):
        """
        """
        super().__init__(size, hash_function)

    def render(self, template_dir = "base", output_dir = "output", file_prefix = "",
        beamer = True, scale = 1):
        """ Render all jinja templates, i.e., generate Tikz illustrations and
        compile these into a final "main.tex" documents loacted in the "output_dir"
        """
        # Load jinja templates
        jinja_templates = self.load_jinja_templates(template_dir)
        # Create directories for generated output
        self.create_directories(output_dir)
        # Render all templates
        self.render_templates(jinja_templates, output_dir, beamer, scale, file_prefix)

    def load_jinja_templates(self, template_dir):
        """ Load the directory that contains the jinja templates
        """
        try:
            jinja_templates = jinja2.Environment(
                autoescape = False,
                loader = jinja2.FileSystemLoader(
                    searchpath = os.path.join(template_dir),
                ),
            )
        except KeyError as e:
            print("INFO : Variable \"template_dir\" not defined!")
            print("Error: ", e)
        return jinja_templates

    def render_template(self, jinja_templates, template_vars, template_name, outfile):
        """
        """
        # Generate configuration and other files according to the given templates
        template = jinja_templates.select_template([template_name])
        with open(outfile, "w") as file:
            print(template.render(**template_vars), file = file)


    def render_templates(self, jinja_templates, output_dir, beamer, scale, prefix):
        """
        """
        # Keep a history of all the Tikz illustrations generated (there is a Tikz
        # illustration for each inserted or searched key)
        steps = {}
        ### Illustrations for all insertion operations
        # Create an illustration for each operation: collision or insertion
        for step in range(1, len(self.history) + 1):
            illustration_name = "insertion_step_" + str(step) + ".tex"
            output_file = os.path.join(output_dir, illustration_name)
            template_vars = self.history[step]
            template_vars["beamer"] = "True" if beamer else "False"
            self.render_template(
                jinja_templates,
                template_vars,
                # The template file to use. Should not be changed:
                "hashtable_insert.tex.jinja", 
                # Specify the correct directory to place the generated file in:
                output_file,
            )
            steps[step] = illustration_name.split(".")[0]
        ### Illustrations for all searching operations
        # TODO: -
        ### Render tikz style template
        output_file = os.path.join(output_dir, "tikz_style.tex")
        template_vars = {}
        self.render_template(
            jinja_templates,
            template_vars,
            # The template file to use. Should not be changed:
            "tikz_style.tex.jinja", 
            # Specify the correct directory to place the generated file in:
            output_file,
        )
        ### Main ".tex" document
        output_file = os.path.join(output_dir, "main.tex")
        template_vars = {
                "steps": steps,
                "tikz_style": "tikz_style",
                "scale": scale,
        }
        self.render_template(
            jinja_templates,
            template_vars,
            # The template file to use. Should not be changed:
            "beamer_main.tex.jinja" if beamer else "article_main.tex.jinja",
            # Specify the correct directory to place the generated file in:
            output_file,
        )

    def create_directories(self, output_dir):
        """ Generate directories
        """
        # Create required output directories if they're missing
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok = True)
