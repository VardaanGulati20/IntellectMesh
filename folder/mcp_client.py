
# import requests
# from logger import sanitize_text, save_to_pdf

# def ask_question(question):
#     try:
#         response = requests.post(
#             "http://localhost:8000/invoke",
#             json={"input": question}
#         )
#         result = response.json()
#     except Exception as e:
#         print(f"❌ Failed to reach MCP server: {e}")
#         return

#     if "error" in result:
#         print(f"❌ MCP Server Error: {result['error']}")
#         return

    
#     initial_answer = result.get("initial_answer", "")
#     critic_feedback_1 = result.get("critic_feedback_1", "")
#     score_1 = result.get("score_1", 0)
#     final_answer = result.get("final_answer", "")
#     critic_feedback_2 = result.get("critic_feedback_2", "")
    
#     score_2 = result.get("score_2", 0)

#     print("\n--- MCP Educational Assistant Output ---")
#     print(f"\n📌 Question:\n{question}")
#     print(f"\n📖 Initial Answer:\n{initial_answer}")
#     print(f"\n🧠 Critic Feedback (Initial Answer):\n{critic_feedback_1} (Score: {score_1})")
#     print(f"\n✅ Final Improved Answer:\n{final_answer}")
#     print(f"\n🧠 Critic Feedback (Final Answer):\n{critic_feedback_2} (Score: {score_2})")

    
#     sections = {
#         "Question": sanitize_text(question),
#         "Initial Answer": sanitize_text(initial_answer),
#         "Critic Feedback (Initial Answer)": sanitize_text(f"{critic_feedback_1} (Score: {score_1})"),
#         "Final Improved Answer": sanitize_text(final_answer),
#         "Critic Feedback (Final Answer)": sanitize_text(f"{critic_feedback_2} (Score: {score_2})"),
#     }

#     save_to_pdf(sections, filename="mcp_output.pdf")

# if __name__ == "__main__":
#     user_question = input("Enter your educational question: ")
#     ask_question(user_question)
# import requests
# from logger import sanitize_text, save_to_pdf

# def ask_question(question):
#     try:
#         response = requests.post(
#             "http://localhost:8080/a2a",  # 🚀 A2A orchestrator endpoint
#             json={"input": question, "context": {}}
#         )
#         result = response.json()
#     except Exception as e:
#         print(f"❌ Failed to reach orchestrator: {e}")
#         return

#     final_answer = result.get("final_answer", "[No answer returned]")

#     # Optional: add intermediate stages if orchestrator returns them
#     print("\n--- MCP A2A Educational Assistant Output ---")
#     print(f"\n📌 Question:\n{question}")
#     print(f"\n✅ Final Answer:\n{final_answer}")

#     # Save to PDF
#     sections = {
#         "Question": sanitize_text(question),
#         "Final Answer": sanitize_text(final_answer)
#     }
#     save_to_pdf(sections, filename="mcp_output.pdf")

# if __name__ == "__main__":
#     user_question = input("Enter your educational question: ")
#     ask_question(user_question)
# import requests
# import sys
# from datetime import datetime
# from fpdf import FPDF

# MCP_SERVER_URL = "http://localhost:8000/ask"

# def ask_question(question: str) -> dict:
#     try:
#         response = requests.post(
#             MCP_SERVER_URL,
#             json={"question": question},
#             timeout=120
#         )
#         return response.json()
#     except Exception as e:
#         return {"error": f"Request failed: {e}"}

# def save_to_pdf(question: str, answer: str, pipeline: str):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)

#     pdf.multi_cell(0, 10, f"🧠 Question:\n{question}\n", align="L")
#     pdf.multi_cell(0, 10, f"📡 Pipeline Used:\n{pipeline}\n", align="L")
#     pdf.multi_cell(0, 10, f"✅ Final Answer:\n{answer}", align="L")

#     filename = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#     pdf.output(filename)
#     print(f"📄 Saved response to: {filename}")

# def main():
#     if len(sys.argv) > 1:
#         question = " ".join(sys.argv[1:])
#     else:
#         question = input("❓ Enter your question: ")

#     result = ask_question(question)

#     if "error" in result:
#         print(f"❌ Error: {result['error']}")
#         return

#     answer = result.get("final_answer", "[No answer returned]")
#     pipeline = result.get("pipeline", "[Unknown pipeline]")

#     print("\n✅ FINAL ANSWER:\n")
#     print(answer)
#     print("\n🔁 Pipeline Used:", pipeline)

#     save_to_pdf(question, answer, pipeline)

# if __name__ == "__main__":
#     main()
# import requests
# from logger import sanitize_text, save_to_pdf

# # Replace with actual running MCP orchestrator endpoint
# SERVER_URL = "http://localhost:8000/ask"

# def ask_question(question):
#     payload = {
#         "question": question
        
#     }

#     try:
#         response = requests.post(SERVER_URL, json=payload)
#         if response.status_code == 200:
#             data = response.json()

#             # Pull structured pipeline fields from server response
#             return {
#                 "scraper_output": data.get("scraper_output", ""),
#                 "critic_feedback_1": data.get("critic_feedback_1", ""),
#                 "refined_output": data.get("refined_output", ""),
#                 "critic_feedback_2": data.get("critic_feedback_2", ""),
#                 "final_answer": data.get("answer", ""),
#                 "pipeline_used": data.get("pipeline", "unknown")
#             }
#         else:
#             print("❌ Server returned error:", response.text)
#             return None
#     except Exception as e:
#         print(f"❌ Failed to connect to server: {e}")
#         return None

# def main():
#     question = input("❓ Enter your question: ").strip()
#     result = ask_question(question)

#     if result:
#         # Print only final answer to terminal
#         print("\n✅ FINAL ANSWER:\n")
#         print(sanitize_text(result["final_answer"]))

#         # Save full reasoning trace to PDF
#         save_to_pdf(
#             question=question,
#             scraper_output=result["scraper_output"],
#             critic_feedback_1=result["critic_feedback_1"],
#             refined_output=result["refined_output"],
#             critic_feedback_2=result["critic_feedback_2"],
#             final_answer=result["final_answer"],
#             pipeline_used=result["pipeline_used"]
#         )

# if __name__ == "__main__":
#     main()
# 📦 Standard Imports
# import requests
# from logger import sanitize_text, save_to_pdf

# # 🎯 Endpoint
# SERVER_URL = "http://localhost:8000/ask"

# # 🧾 Ask user a question
# question = input("Ask a question: ")

# # 🚀 Send to MCP Server
# try:
#     print("\n📡 Sending to MCP server...")
#     response = requests.post(SERVER_URL, json={
#         "input": question,
#         "context": {},
#         "pipeline_trace": []
#     }, timeout=60)

#     data = response.json()

#     # 🖨️ Print only final answer
#     final_answer = data.get("answer", "[No answer returned]")
#     print("\n✅ Final Answer:\n")
#     print(final_answer)

#     # 🧾 Prepare full structured report
#     full_log = f"""
#     🔹 Question: {question}

#     🔹 Final Answer:
#     {data.get("answer", "")}

#     🔸 Phase 1 (Scraper):
#     {data.get('pipeline_trace', [{}])[0].get('content', '')}

#     🔸 Phase 2 (Critic Feedback 1):
#     Score: {data.get('pipeline_trace', [{}])[1].get('score', '?')}
#     Feedback: {data.get('pipeline_trace', [{}])[1].get('feedback', '')}

#     🔸 Phase 3 (LLM Refiner Output):
#     {data.get('pipeline_trace', [{}])[2].get('content', '')}

#     🔸 Phase 4 (Critic Feedback 2):
#     Score: {data.get('score', '?')}
#     Feedback: {data.get('feedback', '')}
#     """

#     sanitized = sanitize_text(full_log)
#     save_to_pdf(sanitized)
#     print("\n📝 Full interaction saved to PDF.")

# except Exception as e:
#     print(f"❌ Request failed: {e}")
# import requests
# from logger import sanitize_text, save_to_pdf

# # 🎯 Endpoint
# SERVER_URL = "http://localhost:8000/ask"

# # 🧾 Ask user a question
# question = input("Ask a question: ")

# # 🚀 Send to MCP Server
# try:
#     print("\n📡 Sending to MCP server...")
#     response = requests.post(SERVER_URL, json={"question": question}, timeout=300)
#     data = response.json()

#     # ✅ Final answer
#     final_answer = data.get("answer", "[No answer returned]")
#     print("\n✅ Final Answer:\n")
#     print(final_answer)

#     # 🧠 Extract trace steps safely
#     trace = data.get("pipeline_trace", [])
#     scraper_output = ""
#     critic_feedback_1 = ""
#     refined_output = ""
#     critic_feedback_2 = ""

#     for step in trace:
#         tool = step.get("tool", "")
#         if tool == "scraper":
#             scraper_output = step.get("output", step.get("content", ""))
#         elif tool == "critic" and step.get("phase") == "initial":
#             critic_feedback_1 = f"Score: {step.get('score')}, Feedback: {step.get('feedback')}"
#         elif tool == "llm":
#             refined_output = step.get("output", step.get("content", ""))
#         elif tool == "critic" and step.get("phase") == "refined":
#             critic_feedback_2 = f"Score: {step.get('score')}, Feedback: {step.get('feedback')}"

#     # 📝 Save to PDF
#     save_to_pdf(
#         question,
#         scraper_output,
#         critic_feedback_1,
#         refined_output,
#         critic_feedback_2,
#         final_answer,
#         pipeline_used=sanitize_text(str(trace))
#     )

#     print("\n📝 Full interaction saved to PDF.")

# except Exception as e:
#     print(f"❌ Request failed: {e}")
# import requests
# import json

# # 🎯 Endpoint
# SERVER_URL = "http://localhost:8000/ask"

# # 🧾 Ask user a question
# question = input("🗨️  Ask a question: ")
# intent = "improve_answer"

# try:
#     print("\n📡 Sending to MCP Server...")
#     response = requests.post(
#         SERVER_URL,
#         json={"question": question, "intent": intent},
#         timeout=300
#     )
#     data = response.json()

#     # ✅ Final Answer
#     final_answer = data.get("answer", "[No answer returned]")
#     print("\n✅ Final Answer:\n")
#     print(final_answer)

#     # 🧠 Display Trace
#     print("\n🧪 Pipeline Trace:")
#     trace = data.get("pipeline_trace", [])
#     for i, step in enumerate(trace):
#         print(f"\n🔧 Step {i+1} - Tool: {step.get('tool')}")
#         for k, v in step.items():
#             if k != "tool":
#                 print(f"   • {k}: {str(v)[:400]}{'...' if len(str(v)) > 400 else ''}")

# except Exception as e:
#     print(f"❌ Request failed: {e}")
import requests
import json

# 🧭 MCP Registry Config
REGISTRY_URL = "http://localhost:9000"
ENTRY_TAG = "entry"  # This should match the tag in mcp_server.py's AGENT_CARD

# 🌐 Resolve the MCP Server /ask endpoint
def resolve_entrypoint():
    try:
        res = requests.get(f"{REGISTRY_URL}/resolve", params={"tag": ENTRY_TAG})
        return res.json().get("endpoints", {}).get("ask")
    except Exception as e:
        print(f"❌ Failed to resolve entrypoint from registry: {e}")
        return None

def main():
    SERVER_URL = resolve_entrypoint()
    if not SERVER_URL:
        print("❌ No server found from registry.")
        return

    # 🧾 Ask user a question
    question = input("🗨️  Ask a question: ") or "Give me a lesson plan on software testing"
    intent = "improve_answer"

    try:
        print("\n📡 Sending to MCP Server...")
        response = requests.post(
            SERVER_URL,
            json={"question": question, "intent": intent},
            timeout=300
        )
        data = response.json()

        # ✅ Final Answer
        final_answer = data.get("answer", "[No answer returned]")
        print("\n✅ Final Answer:\n")
        print(final_answer)

        # 🧠 Display Trace
        print("\n🧪 Pipeline Trace:")
        trace = data.get("pipeline_trace", [])
        for i, step in enumerate(trace):
            print(f"\n🔧 Step {i+1} - Tool: {step.get('tool')}")
            for k, v in step.items():
                if k != "tool":
                    print(f"   • {k}: {str(v)[:400]}{'...' if len(str(v)) > 400 else ''}")

    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    main()
