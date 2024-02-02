"""
This script demonstrates how to use the ProSuite Python API to create a simple quality specification (without a DDX!)
and run a here specified verification on a dataset.

It also demonstrates how to handle issues that are returned from the verification
and how to control the verification process based on the issues.
"""

import prosuite as ps

# 1. Start ProSuite QA microservice (if not already running)

# 2. Create & configure a Verification

model = ps.Model("TopoModel", "D:\Test Data\ExtractStGallen.gdb") # From "ProSuite Documentation / SampleData.zip"
datasets = [ps.Dataset("TLM_FLIESSGEWAESSER", model),
            ps.Dataset("TLM_STRASSE", model)]

service = ps.Service(host_name='localhost', port_nr=5151) # You might want to change this to the host and port of your ProSuite installation

simpleSpecification = ps.Specification(
    name='MinimumLengthSpecification',
    description='A very simple quality specification checking feature and segment length of roads and rivers')

for dataset in datasets:
    simpleSpecification.add_condition(ps.Conditions.qa_min_length_0(dataset, limit=10, is3_d=False))
    simpleSpecification.add_condition(ps.Conditions.qa_segment_length_0(dataset, 1.5, False))

envelope = ps.EnvelopePerimeter(x_min=2750673, y_min=1215551, x_max=2765845, y_max=1206640)

out_dir = 'C:/temp/verification_output' # You might want to change this to a directory that exists on your system, also make sure no Issue.gdb exists in this directory

verification_responses = service.verify(specification=simpleSpecification, output_dir=out_dir, perimeter=envelope)


# 3. Run Verification and handle issues with the Issue Object

issue_allowable = True

for verification_response in verification_responses:
    if len(verification_response.issues) > 0:
        for issue in verification_response.issues:
            # Demo Prints

            # print(issue.description)
            # print(issue.involved_objects)
            # print(issue.geometry)
            # print(issue.issue_code)
            # print(issue.allowable)
            # print(issue.stop_condition)

            if issue.allowable is False:
                print(f"Not allowed issue met: {issue.description} in {issue.involved_objects[0].table_name}")
                print("Stopping verification")
                issue_allowable = False
                break

    if issue_allowable is False:
        break


