from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class
from IPython.display import HTML, display

from amazonregister import AmazonService
from googleregister import GoogleService
from googleapiclient.discovery import build
import ipywidgets as widgets

selected_instance = ""
accordion =""

aws = AmazonService()
compute = build('compute', 'v1')
google = GoogleService()

#create instance button handler
def create_button_clicked(b):
    aws.create_instance()

#terminate instance button handler
def terminate_button_clicked(b):
    global selected_instance
    global accordion
    selected_instance = accordion.selected_index

    aws.terminate_instance(selected_instance)


#toggle instance button handler
def toggle_button_clicked(b):
    global selected_instance
    global accordion
    selected_instance = accordion.selected_index

    aws.toggle_instance(selected_instance)


#terminate instance button handler
def reboot_button_clicked(b):
    global selected_instance
    global accordion
    selected_instance = accordion.selected_index
    aws.reboot_instance(selected_instance)

@magics_class
class TestMagics(Magics):
    @line_magic
    def db(self, line):
        global selected_instance
        global accordion

        instancesFormatted = google.get_instances_info(compute, 'project-guppi-232323', 'us-east1-b')
        
        button = widgets.Button(description="Create Instance")
        display(button)
        button.on_click(create_button_clicked)
        # if user wants to see table view
        if(line == "table"):
            # I create a string 'html' to hold the html view of our table
            # here I am creating the table and loading it with the column headers
            html = "<table><tr>"
            html += "<th>"
            html += 'Name'
            html += "</th>"
            html += "<th>"
            html += 'Instance Id'
            html += "</th>"
            html += "<th>"
            html += 'Instance Type'
            html += "</th>"
            html += "<th>"
            html += 'Availability Zone'
            html += "</th>"
            html += "<th>"
            html += 'State'
            html += "</th>"
            html += "<th>"
            html += 'Key Name'
            html += "</th>"
            html += "<th>"
            html += 'Launch Time'
            html += "</th>"
            html += "</tr>"
            # for each row load in data from AWS
            for row in instancesFormatted:
                html += "<tr>"
                html += "<td>"
                html += row['Name']
                html += "</td>"
                html += "<td>"
                html += row['Instance Id']
                html += "</td>"
                html += "<td>"
                html += row['Instance Type']
                html += "</td>"
                html += "<td>"
                html += row['Availability Zone']
                html += "</td>"
                html += "<td>"
                html += row['State']
                html += "</td>"
                html += "<td>"
                html += row['Key Name']
                html += "</td>"
                html += "<td>"
                html += str(row['Launch Time'])
                html += "</td>"
                html += "</tr>"
            html += "</table>"
            # display html table
            display(HTML(html))
            
        else:
            #stores the info and buttons for each instance
            accordion_children = []

            for row in instancesFormatted:
                #appends all info into array of labels
                info = ["<b>Instance Type:</b>", row['Instance Type'] ,"<b>Availability Zone:</b>", row['Availability Zone'], "<b>State:<b>" , row['State']]

                #makes each label html and puts into HBox
                items = [widgets.HTML(str(i)) for i in info]
                instance_info = widgets.HBox(items)

                #buttons
                
                if(row['State'] == "running"):
                    toggle_button = widgets.Button(description='Stop Instance')
                elif(row['State'] == "stopped"):
                    toggle_button = widgets.Button(description='Start Instance')
                else:
                    toggle_button = widgets.Button(description='Start Instance',disabled=True)

                #disables the terminate button when not running or stopped
                if(row['State'] == "running" or row['State'] == "stopped"):
                    terminate_button = widgets.Button(description='Terminate Instance')
                else:
                    terminate_button = widgets.Button(description='Terminate Instance',disabled=True)
                # reboot button
                if(row['State'] == "running"):
                    reboot_button = widgets.Button(description='Reboot Instance')
                else:
                    reboot_button = widgets.Button(description='Reboot Instance',disabled=True)


                file = open("icons/running.png", "rb")

                if(row['State'] == "running"):
                    file = open("icons/running.png", "rb")
                elif(row['State'] == "pending"):
                    file = open("icons/pending.png", "rb")
                elif(row['State'] == "stopping"):
                    file = open("icons/stopping.png", "rb")
                elif(row['State'] == "stopped"):
                    file = open("icons/stopped.png", "rb")
                elif(row['State'] == "shutting-down"):
                    file = open("icons/shutting-down.png", "rb")
                else:
                    file = open("icons/terminated.png", "rb")

                image = file.read()
                indicator = widgets.Image(value=image,format='png')
                

                toggle_button.on_click(toggle_button_clicked)
                terminate_button.on_click(terminate_button_clicked)
                reboot_button.on_click(reboot_button_clicked)

                buttons = [toggle_button,reboot_button,terminate_button,indicator]
                button_box = widgets.HBox(buttons)

                
                #puts info and buttons into vBox
                instance_box = widgets.VBox([instance_info, button_box])

                #adds it to list of childeren for accordian
                accordion_children.append(instance_box)

            accordion = widgets.Accordion(accordion_children)

            acc_index = 0
            
            #adding titles to the accordian
            for row in instancesFormatted:
                acc_title = row['Instance Id']
                acc_title += " "
                acc_title += row['State']
                accordion.set_title(acc_index, acc_title)
                acc_index += 1

            display(accordion)

            
            #sets global selected instance to currently selected instance
            selected_instance = accordion.selected_index

def load_ipython_extension(ipython):
    """This function is called when the extension is
    loaded. It accepts an IPython InteractiveShell
    instance. We can register the magic with the
    `register_magic_function` method of the shell
    instance."""
    ipython.register_magics(TestMagics)
