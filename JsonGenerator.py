import json
import uuid
import base64

class JsonGenerator:
    def __init__(self):
        self.json_data = {
            "div_list": [],
            "data_grids": [],
            "fields": []
        }
        self.panel_id_counter = 1
        self.data_grid_id_counter = 1
        self.field_id_counter = 1

    def generate_unique_id(self, prefix):
        """Generate a unique ID with the given prefix."""
        return f"{prefix}_{uuid.uuid4().hex}"

    def gather_field_input(self):
        """Gathers user input for a field."""
        data_type = input("Enter the data type for the field (text, number, markdown, html): ")
        
        if data_type.lower() in ['markdown', 'html']:
            file_path = input("Enter the path to the file containing the content: ")
            with open(file_path, 'rb') as f:
                content = f.read()
            content_base64 = base64.b64encode(content).decode('utf-8')
            label = input("Enter the label for the field: ")
            field_id = self.generate_unique_id("field")   # Generate unique ID for the field
                     
            field = {
                "content_id": field_id,
                "data_type": data_type.lower(),
                "label": label,
                "is_editable": "true",
                "is_disabled": "false",
                "is_data_required":"true",
                "o": [
                    {
                        "v": content_base64,
                        "d": None
                    }
                ],
                "m": [
                    {
                        "v": content_base64,
                        "d": None
                    }
                ],
                "functional_attributes": {}
            }  
            return field

        else:
            sub_type = ""
            resize_allowed = ""
            if data_type == "text":
                sub_type = input("Enter the sub type(optional)(email, password, date, time, range): ")  
                # resize_allowed = input("Should the field be resizable (true/false): ")
            
            decimal_places = ""    
            if data_type == "number":
                decimal_places = input("Enter the decimal places: ")  
                min_val = input("Enter the Minimum number: ")
                max_val = input("Enter the Maximum number: ")
            
            label = input("Enter the label for the field: ")
            variant = input("Enter the variant (outlined, filled, standard, contained, text): ")
            # is_editable = input("Should the field be editable? (true/false): ")
            # is_disabled = input("Should the field be disabled? (true/false): ")
            # is_data_required = input("Is data required for the field? (true/false): ")
            # placeholder = input("Enter the placeholder text (optional): ")

            field_id = self.generate_unique_id("field")  # Generate unique ID for the field
                     
            field = {
                "content_id": field_id,
                "data_type": data_type.lower(),
                "label": label,
                "variant": variant,
                "is_editable": "true",
                "is_disabled": "false",
                "is_data_required": "true",
                "o": [
                    {
                        "v": input("Enter the 'o' value for the field: "),
                        "d": None
                    }
                ],
                "m": [
                    {
                        "v": input("Enter the 'm' value for the field: "),
                        "d": None
                    }
                ],
                "functional_attributes": {
                    "placeholder": label,
    
                }
            }  
            if sub_type:
                field["functional_attributes"]["sub_type"] = sub_type
            if resize_allowed:
                field["functional_attributes"]["resize_allowed"]= resize_allowed
                field["functional_attributes"]["rows"] = 3
            if decimal_places:
                field["functional_attributes"]["decimal_places"] = decimal_places
                field["functional_attributes"]["min"] = min_val
                field["functional_attributes"]["max"] = max_val
            return field

    def gather_panel_input(self):
        """Gathers user input for a panel."""
        container_type = input("Enter the container type (panel, accordion, tab_group): ")
        container_text = input("Enter the text for the panel container: ")
        panel_order = len(self.json_data["div_list"]) + 1
        div_list = []
        # panel_id = self.generate_unique_id("panel")
        if container_type == "tab_group":
            num_tabs = int(input("Enter the number of tabs for this tab group: "))
            for i in range(num_tabs):
                tab_order = i + 1
                tab_text = input(f"Enter the text for Tab {tab_order}: ")
                tab_div_list = []
                num_fields = int(input(f"Enter the number of fields for Tab {tab_order}: "))
                for j in range(num_fields):
                    field = self.gather_field_input()
                    self.json_data["fields"].append(field)
                    tab_div_list.append({
                        "order": j + 1,
                        "style": {
                            "responsiveness": {
                                "sm": 6,
                                "md": 6,
                                "lg": 6
                            }
                        },
                        "content": {
                            "content_type": "field",
                            "content_id": field["content_id"]
                        }
                    })
                div_list.append({
                    "order": tab_order,
                    "style": {
                        "container_type": "tab",
                        "container_text": tab_text,
                        "responsiveness": {
                            "sm": 12,
                            "md": 12,
                            "lg": 12
                        }
                    },
                    "content": {
                        "content_type": "div_list",
                        "div_list": tab_div_list
                    }
                })
            panel = {
                "order": panel_order,
                "style": {
                    "container_type": "panel",
                    "container_text": container_text,
                    "responsiveness": {
                        "sm": 12,
                        "md": 12,
                        "lg": 12
                    }
                },
                "content": {
                    "content_type": "div_list",
                    "div_list": [{
                        "order": 1,
                        "style": {
                            "container_type": "tab_group",
                            "responsiveness": {
                                "sm": 12,
                                "md": 12,
                                "lg": 12
                            }
                        },
                        "content": {
                            "content_type": "div_list",
                            "div_list": div_list
                        }
                    }]
                }
            }

        else:
            num_fields = int(input("Enter the number of fields for this panel: "))
            for i in range(num_fields):
                field = self.gather_field_input()
                self.json_data["fields"].append(field)
                div_list.append({
                    "order": i + 1,
                    "style": {
                        "responsiveness": {
                            "sm": 6,
                            "md": 6,
                            "lg": 6
                        }
                    },
                    "content": {
                        "content_type": "field",
                        "content_id": field["content_id"]
                    }
                })
            # Include data grids in the div_list
            num_data_grids = int(input("Enter the number of data grids you want to include in this panel: "))
            for _ in range(num_data_grids):
                data_grid_content_id = self.generate_unique_id("data_grid")
                div_list.append({
                    "order": len(div_list) + 1,
                    "style": {
                        "responsiveness": {
                            "sm": 12,
                            "md": 12,
                            "lg": 12
                        }
                    },
                    "content": {
                        "content_type": "data_grid",
                        "content_id": data_grid_content_id
                    }
                })

            panel = {
                "order": panel_order,
                "style": {
                    "container_type": container_type,
                    "container_text": container_text,
                    "responsiveness": {
                        "sm": 12,
                        "md": 12,
                        "lg": 12
                    }
                },
                "content": {
                    "content_type": "div_list",
                    "div_list": div_list
                }
            }
        return panel
    def gather_data_grid_input(self):
        """Gathers user input for a data grid."""
        content_id = self.generate_unique_id("data_grid")
        title = input("Enter the title for the data grid:")
        is_checkbox_selection = "true"#input("Enable checkbox selection? (true/false): ").lower() == "true"
        sticky_header = "true"# input("Enable sticky header? (true/false): ").lower() == "true"
        table_size = "large"#input("Enter the table size (small, medium, large): ")
        pagination = "false"#input("Enable pagination? (true/false): ").lower() == "true"

        toolbar_options = []
        num_toolbar_options = int(input("Enter the number of toolbar options for the data grid: "))
        for _ in range(num_toolbar_options):
            content_id = ""
            variant= "contained"
            label = input("Enter the label for the toolbar option: ")
            icon = "views-100"#input("Enter the icon name for the toolbar option: ")
            icon_group_id = "icon-group-grid-table"
            button_group = [{
            "content_id": "",
            "label": input("Enter the button label: "),
            "icon": "table-grid-100",
            "actionable_attributes": {
                "actionable_location": "data_grid_toolbar",
                "action_type": "navigation",
                "special_button_type": None,
                "button_scope": "backend",
                "is_action_refresh_when_complete": True,
                "form_field_attributes": None,
                "data_grid_toolbar_attributes": {
                    "rows_sent_type": "selected",
                    "is_row_key_values_required": True,
                    "rows_type": "none"
                },
                "data_grid_row_attributes": None,
                "navigation_attributes": {
                    "navigation_workflow_step_id": "wf-4",
                    "navigation_type": "popup"
                },
                "info_only_attributes": None
            }
        }]

            toolbar_options.append({"label": label,"variant":variant, "icon": icon,"icon_group_id":icon_group_id, "button_group": button_group})

        column_definitions = []
        
        # columns_value = {'Booking Date':{'data_type':'date_time'},
        #                  'Action Required':{'data_type':'text_option'},
        #                  'AGENT/AGL MESSAGING':{'data_type':'text_option'},
        #                  'Booking Status':{'data_type':'text_option'},
        #                  'Assigned Agent':{'data_type':'text'},
        #                  'Importer/Exporter Name':{'data_type':'text'},
        #                  'Consignee (Receiving Customer)':{'data_type':'text'},
        #                  'PO Number':{'data_type':'number'},
        #                  'Factory/Shipper':{'data_type':'text'},
        #                  'Commodity':{'data_type':'text'},
        #                  'FCL/LCL':{'data_type':'text_option'},
        #                  'Requested Containers':{'data_type':'number'},
        #                  'Container Size':{'data_type':'number'},
        #                  'Port of Loading (City, Country)':{'data_type':'text'},
        #                  'Port of Discharge (City, State)':{'data_type':'text'},
        #                  'Customer Final Destination (City, State)':{'data_type':'text'},
        #                  'Carrier Routing Destination (City, State)':{'data_type':'text'},
        #                  'Cargo Ready Date':{'data_type':'date_time'},
        #                  'ETD from Port of Load':{'data_type':'date_time'},
        #                  ' ETA Port of Discharge':{'data_type':'date_time'},
        #                  'Carrier':{'data_type':'text'},
        #                  'RATE EXPIRE DATE':{'data_type':'date_time'},
        #                  'Mitigated Premium':{'data_type':'number'},
        #                  'Carrier Service Fee':{'data_type':'number'},
        #                  'OF Cost Per Container':{'data_type':'number'},
        #                  'Total Cost Per Contianer':{'data_type':'number'},
        #                  'ESTIMATED TRANSIT TIME CY-CY':{'data_type':'date_time'},
        #                  'Contract Free Time':{'data_type':'text'},
        #                  'AGENT BOOKING NUMBER':{'data_type':'text'},
        #                  'AGL Operator':{'data_type':'date_time'},
        #                  'SO Released to Shipper Date':{'data_type':'date_time'},
        #                  'Carrier Booking Number':{'data_type':'text'},
        #                  'Confirmed Carrier':{'data_type':'text'},
        #                  'Confirmed Vessel Name':{'data_type':'text'},
        #                  'Confirmed Vessel Voyage':{'data_type':'number'},
        #                  'Confirmed ETD Port of Loading':{'data_type':'number'},
        #                  'Confirmed ETA Port of Discharge Date':{'data_type':'date_time'},
        #                  'Confirmed Ocean Freight Cost':{'data_type':'number'}}
        columns_value = {'Purchase Order Number':{'data_type':'text'},
                         'Supplier':{'data_type':'text'},
                         'Order Date':{'data_type':'date_time'},
                         'Delivery Date':{'data_type':'date_time'},
                         'Items/Description':{'data_type':'date_time'},
                         'Quantity':{'data_type':'number'},
                         'Unit Price':{'data_type':'number'},
                         'Total Price':{'data_type':'number'},
                         'Status':{'data_type':'text_option'},
                         'Payment Terms':{'data_type':'number'},
                         'Shipping Information':{'data_type':'text'},
                         'Billing Information':{'data_type':'text'},
                         'Approval Status':{'data_type':'text_option'},
                         'Comments/Notes':{'data_type':'text'}}
        functional_attribute = {
        "number":{ 
            # "display_type": "progress_bar",
            "icon_group_id": "icon-group-1",
            "icon_fill": "diamond-filled-100",
            "icon_unfilled": "diamond-unfilled-100",
            # "icon_fill": "star-filled-not-exists",
            # "icon_unfilled": "star-filled-not-exists",
            "defualt_value": None,
            "decimal_separator": None,
            "decimal_places": 0,
            "is_percent": False,
            "prefix": "",
            "postfix": "",
            "is_float_allowed": False
            },
    "image":{
            "display_as": "contain"
    },
    "icon":{
            "icon_group_id": "icon-group-1",
            "display_type": "rating",
            "icon_fill": "cruise-filled-100",
            "icon_unfilled": "cruise-unfilled-100"
          
    },
    "text":{
            "display_type": "textIcon",
            "edit_type": "pick_list",
            "icon_group_id": "icon-group-1",
            "icon_placement": "start_of"
        },
    "text_option":{
            "display_type": "textIcon",
            # "display_type": "chip",
            # "placeholder": "Add Status",
            "edit_type": "pick_list",
            "options_type": "local",
            "options": [
              {
                "value": "approved",
                "display_as": "Approved",
                "icon": "approved",
                # "icon": "bookmark-green",
                "chip_type": "outlined",
                "chip_border_color": "#CD853F",
                "chip_color": "#FF1493",
              },
              {
                "value": "rejected",
                "display_as": "Rejected",
                "icon": "rejected",
                # "icon": "bookmark-green",
                "chip_type": "outlined",
                "chip_border_color": "#CD853F",
                "chip_color": "#FF1493",
                
              },
             
            ],
            "icon_group_id": "icon-group-1",
            "placeholder": "Select Item",
            "icon_placement": "start_of"
        },
    "date_time":{
            "date_time_type": "date",
            "date_time_format": "YYYY-MM-DD",
            "show_timezone": True
    },
    "actions":{
        "display_type": "actions",
        "edit": True,
        "delete": True
    }
    
}
        for column, attributes in columns_value.items():
            data_type = attributes.get('data_type')
         
            attributes_info = functional_attribute[data_type]
            column = {
                "content_id": column,
                "content_name":column, #input("Enter the content name for the column: "),
                "label": column ,#input("Enter the label for the column: "),
                "tooltip_description":column,# input("Enter the tooltip description for the column: "),
                "type":  data_type,#input("Enter the type for the column (number, text, etc.): "),
                "styles": {
                    "width": '120'#int(input("Enter the width for the column: "))
                },
                "is_editable": 'true',#input("Is the column editable? (true/false): ").lower() == "true",
                "align": 'left',#input("Enter the alignment for the column: "),
                "header_align": 'left',#input("Enter the header alignment for the column: "),
                "is_sortable": 'true',#input("Enable sorting for the column? (true/false): ").lower() == "true",
                "default_sort": 'asc',#input("Enter the default sort for the column (asc/desc): "),
                "is_filterable": 'true',#input("Enable filtering for the column? (true/false): ").lower() == "true",
                "is_hidden": 'false',#input("Is the column hidden? (true/false): ").lower() == "true"
                "functional_attributes": 
                    attributes_info
                
            }
            column_definitions.append(column)

        data_grid = {
            "content_id": content_id,
            "grid_options": {
                "title": title,
                "is_checkbox_selection": is_checkbox_selection,
                "sticky_header": sticky_header,
                "table_size": table_size,
                "pagination": pagination,
                "toolbar_options": toolbar_options
            },
            "column_definitions": column_definitions
        }
        return data_grid

    def generate_json(self):
        """Gathers user input and constructs the specific JSON structure."""
        num_panels = int(input("Enter the number of panels you want to create: "))
        for _ in range(num_panels):
            panel = self.gather_panel_input()
            self.json_data["div_list"].append(panel)
            
        num_data_grids = int(input("Enter the number of data grids you want to create: "))
        for _ in range(num_data_grids):
            data_grid = self.gather_data_grid_input()
            self.json_data["data_grids"].append(data_grid)

    def get_json_string(self):
        """Generate and return the JSON string."""
        # return json.dumps(self.json_data, indent=4)
        return self.json_data


# Create an instance of the JsonGenerator class
json_generator = JsonGenerator()

# Call the generate_json method to gather user input and construct the JSON structure
json_generator.generate_json()

json_string = json_generator.get_json_string()
# print(json_string)
json_output_file = 'json_string.json'
with open(json_output_file, 'w') as json_file:
    json.dump(json_string, json_file, indent=4)

# print("JSON data has been generated and saved to:", json_string)

