# -*- coding: utf-8 -*-

import arcpy
import xml.etree.ElementTree as ET

param_xml_file_index = 0
param_specification_name_index = 1
param_data_source_table = 2

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [XmlBasedVerification]

class XmlBasedVerification(object):

    def __init__(self):
        self.label = "XML-based verification"
        self.description = "Here description bla bla...."
        self.category = "ProSuite QA"
        self.canRunInBackground = False

    def getParameterInfo(self):

        params = []

        # Define XML input parameter
        param_xml = arcpy.Parameter(
            displayName="XML File",
            name="xml_file",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")
        
        param_xml.filter.list = ["xml"]

        params.append(param_xml)

        # The specification name dropdown
        param_spec_name = arcpy.Parameter(
            displayName="Quality Specification Name",
            name="specification_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_spec_name.filter.type = "ValueList"

        params.append(param_spec_name)

        # Define data sources input parameter
        param_data_sources = arcpy.Parameter(
            displayName="Key-Value Pairs",
            name="kv_pairs",
            datatype="GPValueTable",
            enabled=True,
            parameterType="Required",
            direction="Input")

        param_data_sources.parameterDependencies = [param_xml.name]

        # Define key field for the GPValueTable parameter
        param_data_sources.columns = [["GPString", "Workspace ID"], ["DEWorkspace", "Workspace Path"]]
        param_data_sources.keyFieldNames = ["Key"]

        # param_data_sources.editable = True
        # param_data_sources.setEditable(1, True)

        params.append(param_data_sources)

        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        if parameters[param_xml_file_index].value:
            xml_file = parameters[param_xml_file_index].valueAsText
            try:
                # Parse the XML file 
                tree = ET.parse(xml_file)
                root = tree.getroot()

                # Get the specification names (TODO: make test, does not alway work)
                namespaces = { 'default': 'urn:ProSuite.QA.QualitySpecifications-3.0', }
                quality_specifications = root.findall('.//default:QualitySpecification', namespaces) 
                
                specification_names = []
                for quality_spec in quality_specifications: 
                    name = quality_spec.get('name')
                    arcpy.AddWarning(f"Spec name: {name}")
                    specification_names.append(name)

                parameters[param_specification_name_index].filter.list = specification_names
                parameters[param_specification_name_index].value = specification_names[0] if specification_names else ""


                # TODO: Depending on the selected specification name, get the relevant (referenced) workspace IDs
                # workspace_uuid = quality_spec.find('.//default:Dataset', namespaces).get('workspace') 
                # workspace_element = root.find('.//default:Workspace[@id="{}"]'.format(workspace_uuid), namespaces) 
                # workspace_id = workspace_element.get('id') 
                # print("Quality Specification Name:", name) 
                # print("Workspace ID:", workspace_id) 
                # print("---------------------")
                keys = set()
                for element in root.iter():
                    keys.add(element.tag)
                
                # Update the choices for key field in the GPValueTable parameter
                parameters[param_data_source_table].values = [[key, ""] for key in keys]
                
                # for datasource_id in keys:
                #     parameters[1].addRow(datasource_id)
            
            except Exception as e:
                parameters[param_data_source_table].values = []
                arcpy.AddWarning(f"Error occurred while parsing the XML file: {str(e)}")

        return

    def execute(self, parameters, messages):
        xml_file = parameters[0].valueAsText
        kv_pairs = parameters[1].values

        try:
            # Parse the XML file and extract key-value pairs
            tree = ET.parse(xml_file)
            root = tree.getroot()
            extracted_pairs = {}

            for element in root.iter():
                for kv_pair in kv_pairs:
                    if element.tag == kv_pair[0]:
                        extracted_pairs[kv_pair[0]] = kv_pair[1]

            # Print the extracted key-value pairs
            for key, value in extracted_pairs.items():
                arcpy.AddMessage(f"{key}: {value}")

        except Exception as e:
            arcpy.AddError(f"Error occurred while parsing the XML file: {str(e)}")

        return
    
