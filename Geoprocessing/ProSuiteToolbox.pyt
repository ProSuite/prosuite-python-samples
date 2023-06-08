# -*- coding: utf-8 -*-

import arcpy
import xml.etree.ElementTree as ET

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
        # Define XML input parameter
        param_xml = arcpy.Parameter(
            displayName="XML File",
            name="xml_file",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")

        # Define data sources input parameter
        param_data_sources = arcpy.Parameter(
            displayName="Key-Value Pairs",
            name="kv_pairs",
            datatype="GPValueTable",
            parameterType="Required",
            direction="Input")

        param_data_sources.parameterDependencies = [param_xml.name]

        # Define key field for the GPValueTable parameter
        param_data_sources.columns = [["GPString", "Workspace ID"], ["GPString", "Workspace Path"]]
        param_data_sources.keyFieldNames = ["Key"]
        # param_data_sources.editable = True
        # param_data_sources.setEditable(1, True)

        params = [param_xml, param_data_sources]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        if parameters[0].value:
            xml_file = parameters[0].valueAsText
            try:
                # Parse the XML file and get the available keys
                tree = ET.parse(xml_file)
                root = tree.getroot()
                keys = set()
                for element in root.iter():
                    keys.add(element.tag)
                
                # Update the choices for key field in the GPValueTable parameter
                parameters[1].values = [[key, ""] for key in keys]
                
                # for datasource_id in keys:
                #     parameters[1].addRow(datasource_id)
            
            except Exception as e:
                parameters[1].values = []
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
    
