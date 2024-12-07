import logging
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class InformationGenerator:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        try:
            # Load FLAN-T5 model and tokenizer
            model_name = "google/flan-t5-base"  # Options: base, large, xl, or xxl
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            self.logger.info("FLAN-T5 model loaded successfully.")
        except Exception as e:
            self.logger.error(f"Error initializing FLAN-T5 model: {e}")
            self.tokenizer = None
            self.model = None

    def generate_answer(self, question, results):
        """
        Generate a coherent paragraph answering the question using the provided results.

        Parameters:
        question (str): The user's query.
        results (list[dict]): A list of dictionaries containing supplemental information.

        Returns:
        str: A coherent paragraph answering the question.
        """
        try:
            # Combine question and results into a single input text
            input_text = f"Question: {question}\nInformation: {' '.join([r['text'] for r in results])}"
            
            # Tokenize the input
            inputs = self.tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512)

            # Generate a coherent paragraph
            if self.model:
                outputs = self.model.generate(
                    inputs["input_ids"],
                    max_new_tokens=200,
                    num_return_sequences=1,
                    no_repeat_ngram_size=3
                )
                generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                return generated_text.strip()
            else:
                return "Model not available. Unable to generate coherent text."

        except Exception as e:
            self.logger.error(f"Error generating answer: {e}")
            return "Error generating answer."

    def generate_report(self, extracted_info):
        """
        Create a full report based on multiple questions and their results.

        Parameters:
        extracted_info (list[dict]): A list containing query and results pairs.

        Returns:
        str: The generated report as a string.
        """
        try:
            report = []
            for info in extracted_info:
                question = info.get("query", "No question provided")
                results = info.get("results", [])

                # Generate an answer for each question
                paragraph = self.generate_answer(question, results)
                self.logger.info(f"Generated answer for question: {question}")
                report.append(paragraph)

            return "\n\n".join(report)
        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
            return "Error generating report."

    def save_report(self, report: str, output_filepath: str):
        """
        Save the generated report to a file.

        Parameters:
        report (str): The report text to save.
        output_filepath (str): The path to the output file.
        """
        try:
            with open(output_filepath, "w", encoding='utf-8') as file:
                file.write(report)
            self.logger.info(f"Report saved to {output_filepath}")
        except Exception as e:
            self.logger.error(f"Error saving report: {e}")

# Example of how to use the generator
def Generate_Main(all_extracted_info):
    output_report_filepath = "generated_report.txt"
    generator = InformationGenerator()
    
    # Generate the report using the extracted information
    report = generator.generate_report(all_extracted_info)
    
    # Save the report to a file
    generator.save_report(report, output_report_filepath)

# Example input format
if __name__ == "__main__":
    Generate_Main()
