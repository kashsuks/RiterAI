import json
import sys
import logging
from transformers import pipeline

class InformationGenerator:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        try:
            self.text_generator = pipeline("text-generation", model="gpt2", tokenizer="gpt2", framework="pt")
        except Exception as e:
            self.logger.error(f"Error initializing NLP model: {e}")
            self.text_generator = None

    def generate_coherent_paragraph(self, question, results):
        try:
            input_text = f"Question: {question}\nResults: {' '.join([r['text'] for r in results])}\nGenerated: "
            if self.text_generator:
                generated_text = self.text_generator(input_text, truncation=True, max_new_tokens=200, num_return_sequences=1)[0]['generated_text']
                return generated_text.strip()
            else:
                return "NLP model not available. Unable to generate coherent text."
        except Exception as e:
            self.logger.error(f"Error generating paragraph: {e}")
            return "Error generating coherent text."

    def generate_report(self, extracted_info):
        try:
            report = []
            for info in extracted_info:
                question = info.get("query", "No question")
                results = info.get("results", [])

                paragraph = self.generate_coherent_paragraph(question, results)
                print(paragraph)
                report.append(paragraph)

            return "\n\n".join(report)
        
        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
            return "Error generating report."

    def save_report(self, report: str, output_filepath: str):
        try:
            with open(output_filepath, "w", encoding='utf-8') as file:
                file.write(report)
            self.logger.info(f"Report saved to {output_filepath}")
        except Exception as e:
            self.logger.error(f"Error saving report: {e}")

def Generate_Main(all_extracted_info):
    output_report_filepath = "generated_report.txt"
    generator = InformationGenerator()
    report = generator.generate_report(all_extracted_info)
    generator.save_report(report, output_report_filepath)

if __name__ == "__main__":
    Generate_Main()
