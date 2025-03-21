 "messages": [
                {
                    "role": "system",
                    "content": (
                        f"""
                        ##################### CONTEXT ####################  
                        You are a domain expert assistant specializing in mapping clinical tabular data to FHIR resources (FHIR R4).  
                        You have been given information about table attributes (including their names, descriptions, and sample values) and your task is to determine the 3 most specific FHIR attributes that best correspond to each table attribute. You may choose attributes from any FHIR resource as you see fit.  

                        Review the given attributes thoroughly and choose the mappings that most accurately reflect the semantic meaning and structure of the table attributes in the context of FHIR. Reason about the potential matches internally, but do not include the reasoning steps in the final answer.
                        The documents you have to consider to answer the query is: {context}
                        ##################### TASK ####################  
                        Based on the provided table attribute information and standard FHIR attribute definitions, determine the top 3 most specific FHIR attributes that correspond to each table attribute, listed in order of relevance (most specific first).
                    
                        ##################### OUTPUT FORMAT ####################  
                        Provide your answer as a JSON object, using the following structure:

                        
                                    "table_attribute_name": "attributeName",
                                    "fhir_attribute_name": "FHIRResource.attributeName 1", "FHIRResource.attributeName 2", "FHIRResource.attributeName 3"
                        

                        Each key corresponds to the table attribute name, and its value is an array of exactly three strings. If fewer than three matches are found, use "No additional attribute found" to fill the empty slots.

                        ##################### EXAMPLE ####################  
                        For example, if the table attribute is "patient_birthDate":

                        
                            "table_attribute_name": "patient_birthDate",
                            "fhir_attribute_name": "Patient.birthDate", "Encounter.birthDate", "Patient.anchorAge"
                        

                        ##################### ADDITIONAL INSTRUCTIONS ####################  
                        - Consider the attribute name, description, and sample values when determining the best FHIR attributes.
                        - Return only the final JSON object without additional commentary.
                        - Use the FHIR R4 specification as the reference (https://www.hl7.org/fhir/).
                        - Double-check your mappings before returning the final result.
                        """
                        
                    )
                },
                {
                    "role": "user",
                    "content": f"{query}"
                }
            ],
            "temperature": 0,
            "top_p": 0,
            "functions": functions,
            "function_call": "auto"
        }


 response = send_request(payload, GPT4V_ENDPOINT)
        print(response)
        response_message = response['choices'][0]['message']
        if 'function_call' in response_message:
            response_content = response_message['function_call']['arguments']
        else:
            response_content = response_message['content']

for i in range(iterations):
            reflection_payload = {
                "messages": [
                    {"role": "system", "content": f"Iteration {i+1}: Initial mapping of top 3 attributes for each column."},
                    {"role": "assistant", "content": response_content},
                    {
                        "role": "system",
                        "content": (
                            f"""
                            #######CONTEXT#######
                            You are a domain expert assistant specializing in mapping clinical tabular data to FHIR resources (FHIR R4). 
                            You have been given information about table attributes (including their names, descriptions, and sample values) and your task is to determine the 3 most specific FHIR attributes that best correspond to each table attribute. You may choose attributes from any FHIR resource as you see fit.
                            You previously provided a mapping between table column names and the top 3 FHIR resource attributes based on similarity.
                            {response_content}
                            #######INPUT_DATA#######
                            The documents you have to consider to answer the query is: {context}
                            #######TASK#######
                            Review the mapping above for completeness and accuracy. Ensure the three best-matched attributes are selected.
                            #######OUTPUT_FORMAT#######
                            Provide your answer as a JSON object in the following format:
                                    {{
                                    "table_attribute_name": "attributeName",
                                    "fhir_attribute_name": "FHIRResource.attributeName 1", "FHIRResource.attributeName 2", "FHIRResource.attributeName 3"
                                    }}
                            """
                            

                        )
                    },
                ],
                "temperature": 0,
                "top_p": 0,
                "functions": functions,
                "function_call": "auto"
            }


  # Construir la consulta para todos los atributos del cluster
    query = "##################### INPUT DATA ##################\n"
    for attr_info in attr_infos:
        attribute_name = attr_info.get("Attribute name")
        description = attr_info.get("Description")
        values = attr_info.get("Values")
        query += f"Attribute Name: {attribute_name}\n"
        query += f"Description: {description}\n"
        query += f"Sample Values: {values}\n"
        query += "----------------------------------------\n"


    query += """
    ##################### TASK ##################
    Based on the provided attribute information and the FHIR attribute definitions, determine the most specific FHIR attribute that corresponds to each table attribute. Be as precise as possible in your mapping.
    ##################### OUTPUT FORMAT ##################
    Provide your answer as a JSON object in the following format:
         {
         "table_attribute_name": "attributeName",
         "fhir_attribute_name": "FHIRResource.attributeName 1", "FHIRResource.attributeName 2", "FHIRResource.attributeName 3"
         },
         {
         "table_attribute_name": "attributeName",
         "fhir_attribute_name": "FHIRResource.attributeName 1", "FHIRResource.attributeName 2", "FHIRResource.attributeName 3"
         },

    }
    """

