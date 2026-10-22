import os
import re
import urllib.parse
from flask import Flask, render_template, request, jsonify, send_file
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun
from docx import Document

app = Flask(__name__, template_folder='templates')

# Configuration
local_model = "ollama/qwen2.5-coder:7b"
search_tool = DuckDuckGoSearchRun()

# Persistent document memory
document_storage = {
    "topic": "",
    "sections": []
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate-section', methods=['POST'])
def generate_section():
    try:
        data = request.json or {}
        topic = data.get('topic', '').strip()
        heading = data.get('heading', '').strip()

        if not topic or not heading:
            return jsonify({'error': 'Please enter both Topic and Section Heading!'}), 400

        document_storage["topic"] = topic

        # Live web research
        search_query = f"{topic} {heading}"
        print(f"Searching web for: {search_query}")
        try:
            search_results = search_tool.run(search_query)
        except Exception as search_err:
            search_results = "No internet search results available, rely on core domain knowledge."

        # Dedicated Agent with Visual Structure Guidance
        researcher_writer = Agent(
            role="Expert Academic Researcher & Writer",
            goal=f"Write a comprehensive academic section for '{heading}' based on the topic '{topic}'. Include visual structure descriptions, timelines, or charts where applicable.",
            backstory="You are an elite academic researcher who constructs rigorous academic content, complete with methodologies, structural frameworks, and references in formal English.",
            tools=[],
            verbose=False,
            llm=local_model
        )

        task_description = f"""
        Research Topic: {topic}
        Section Heading: {heading}
        
        Real-time Web Research Context:
        {search_results}
        
        Instructions: Write a high-quality academic section for '{heading}' in proper academic English. 
        If writing Methodology, Architecture, Timeline, or Budget, describe system flows or data structures clearly using markdown diagrams or structured tables.
        Avoid returning raw JSON schemas.
        """

        section_task = Task(
            description=task_description,
            expected_output=f"Comprehensive academic text for {heading}.",
            agent=researcher_writer
        )

        section_crew = Crew(
            agents=[researcher_writer],
            tasks=[section_task],
            process=Process.sequential
        )

        # Agent Execution
        res = section_crew.kickoff()
        output_text = str(res)

        # Append visual image placeholder if section is Timeline, Budget, or Methodology
        image_url = None
        if "timeline" in heading.lower() or "budget" in heading.lower():
            encoded_title = urllib.parse.quote(f"{topic} - {heading}")
            image_url = f"https://quickchart.io/chart?bkg=white&c={{type:'bar',data:{{labels:['Phase 1','Phase 2','Phase 3','Phase 4'],datasets:[{{label:'{heading}',data:[25,50,75,100]}}]}}}}"

        # Save to memory
        document_storage["sections"].append((heading, output_text, image_url))

        return jsonify({
            'status': 'success',
            'heading': heading,
            'content': output_text,
            'image_url': image_url
        })

    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({'error': f'Backend Error: {str(e)}'}), 500

@app.route('/api/export-docx', methods=['POST'])
def export_docx():
    topic = document_storage.get("topic", "Research_Proposal")
    sections = document_storage.get("sections", [])

    if not sections:
        return jsonify({'error': 'No content available to export!'}), 400

    doc = Document()
    doc.add_heading(f"Research Proposal: {topic.title()}", level=0)

    for item in sections:
        sec_title = item[0]
        sec_text = item[1]
        
        doc.add_heading(sec_title, level=2)
        for paragraph in sec_text.split('\n'):
            if paragraph.strip():
                doc.add_paragraph(paragraph.strip())

    filename = "final_research_proposal.docx"
    filepath = os.path.abspath(filename)
    doc.save(filepath)

    return send_file(filepath, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    print("\n🚀 Server Active with Visual Support! Open Browser: http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000, threaded=True)