import logging
import json
import numpy as np
import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

def numpy_serializer(obj):
    """
    Custom JSON serializer to handle NumPy types

    Args:
        obj: Object to be serialized

    Returns:
        Serializable representation of the object
    """
    if isinstance(obj, np.float32):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def Generate_Main(all_extracted_info):
    """
    Generate a comprehensive report from extracted information

    Args:
        all_extracted_info (list): List of extracted information dictionaries

    Returns:
        str: Generated report text
    """
    try:
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        # Combine results into a single report
        report_text = ""
        for info in all_extracted_info:
            query = info.get('query', 'No query')
            report_text += f"Query: {query}\n"

            for result in info.get('results', []):
                # Convert score to float if it's a NumPy type
                score = float(result.get('score', 'N/A')) if hasattr(result.get('score'), '__float__') else result.get('score')
                report_text += f"Relevant Snippet (Score: {score}): {result.get('text', '')}\n"

            report_text += "\n---\n\n"

        # Save the report
        output_report_filepath = "generated_report.txt"
        with open(output_report_filepath, "w", encoding='utf-8') as file:
            file.write(report_text)

        # Save as JSON with custom serialization
        output_json_filepath = "generated_report.json"
        with open(output_json_filepath, "w", encoding='utf-8') as file:
            json.dump(all_extracted_info, file, indent=2, default=numpy_serializer)

        logger.info(f"Report generated and saved to {output_report_filepath}")
        logger.info(f"JSON report saved to {output_json_filepath}")

        return report_text

    except Exception as e:
        logging.error(f"Error generating report: {e}")
        return ""


def format_report(json_file):
    """
    Formats a JSON report into a readable text format.

    Args:
        json_file (str): Path to the input JSON file
    """
    try:
        # Read the JSON report
        with open(json_file, 'r', encoding='utf-8') as f:
            report = json.load(f)

        # Extract and format the data
        answers = []
        for query_block in report:
            query = query_block.get("query", "No query found")
            answers.append(f"**Query:** {query}\n")

            results = query_block.get("results", [])
            for idx, result in enumerate(results, 1):
                source = result.get("source", "Unknown source")
                text = result.get("text", "").strip()
                answers.append(f"{idx}. Source: {source}\n   {text}\n")

        # Print formatted text to console
        formatted_text = "\n\n".join(answers)
        print(formatted_text)

    except Exception as e:
        print(f"Error formatting report: {e}")


def generate_paragraph_answers(json_file):
    """
    Generates paragraph responses for each query using the query as the question
    and the text from all results as the context, using a local model.

    Args:
        json_file (str): Path to the JSON report file
    """
    try:
        # Load the GPT-2 model and tokenizer
        model_name = "gpt2"  # You can replace with other models like 'EleutherAI/gpt-neo-1.3B'
        model = GPT2LMHeadModel.from_pretrained(model_name)
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)

        # Read the JSON report
        with open(json_file, 'r', encoding='utf-8') as f:
            report = json.load(f)

        paragraph_responses = []
        for query_block in report:
            query = query_block.get("query", "No query found")
            results = query_block.get("results", [])
            context = " ".join(result.get("text", "").strip() for result in results)

            # Check if context is available
            if context:
                # Refined input for better English answers
                input_text = f"""
                **Question:** {query}
                **Context:** {context}
                **Task:** Based on the provided context, please answer the question in a well-structured, comprehensive, and grammatically correct paragraph. 
                Ensure the response is coherent, clear, and free of errors. The answer should be complete and logically consistent, summarizing the key points from the context.
                """

                # Tokenize and generate text
                inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=1024, truncation=True)
                
                # Set pad_token_id to eos_token_id and attention_mask to handle padding tokens properly
                attention_mask = torch.ones(inputs.shape, dtype=torch.long)  # attention mask for padding tokens
                output = model.generate(inputs, attention_mask=attention_mask, pad_token_id=tokenizer.eos_token_id, 
                        max_length=1024, num_return_sequences=1, num_beams=2, no_repeat_ngram_size=2, early_stopping=True)
                


                # Decode and save the result
                answer = tokenizer.decode(output[0], skip_special_tokens=True).strip()
                str(answer)
                paragraph_responses.append(f"**Question:** {query}\n**Answer:** {answer}\n")

            else:
                paragraph_responses.append(f"**Question:** {query}\n**Answer:** No relevant information found.\n")

        # Print only the final answers
        for response in paragraph_responses:
            print(response)

    except Exception as e:
        print(f"Error generating paragraph answers: {e}")


# Allow direct script execution for testing

# Path to the generated_report.json
input_file = "generated_report.json"

# Check if the generated_report.json exists
if os.path.exists(input_file):
    print("Generating paragraph answers...")
    generate_paragraph_answers(input_file)
else:
    print(f"Input file '{input_file}' not found. Please ensure the report is generated.")
