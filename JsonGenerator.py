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
        self.field_id_counter = 1  # Initialize a counter for generating unique field IDs

    def generate_unique_field_id(self):
        """Generate a unique ID for each field."""
        field_id = f"field_{self.field_id_counter}"
        self.field_id_counter += 1
        return field_id

    def gather_field_input(self):
        """Gathers user input for a field."""
        data_type = input("Enter the data type for the field (text, number, markdown, html): ")
        
        if data_type.lower() in ['markdown', 'html']:
            file_path = input("Enter the path to the file containing the content: ")
            with open(file_path, 'rb') as f:
                content = f.read()
            content_base64 = base64.b64encode(content).decode('utf-8')
            label = input("Enter the label for the field: ")
            # is_editable = input("Should the field be editable? (true/false): ")
            # is_disabled = input("Should the field be disabled? (true/false): ")
            # is_data_required = input("Is data required for the field? (true/false): ")

            field_id = self.generate_unique_field_id()  # Generate unique ID for the field
                     
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

            field_id = self.generate_unique_field_id()  # Generate unique ID for the field
                     
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
        if container_type == "tab_group":
            num_tabs = int(input("Enter the number of tabs for this tab group: "))
            div_list = []
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
            div_list = []
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

    def generate_json(self):
        """Gathers user input and constructs the specific JSON structure."""
        num_panels = int(input("Enter the number of panels you want to create: "))

        for _ in range(num_panels):
            panel = self.gather_panel_input()
            self.json_data["div_list"].append(panel)

    def get_json_string(self):
        """Generate and return the JSON string."""
        return json.dumps(self.json_data, indent=4)


# Create an instance of the JsonGenerator class
json_generator = JsonGenerator()

# Call the generate_json method to gather user input and construct the JSON structure
json_generator.generate_json()

json_string = json_generator.get_json_string()
print(json_string)
