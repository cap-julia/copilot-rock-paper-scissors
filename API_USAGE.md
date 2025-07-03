# To run the REST API server, use:
#   uvicorn api:app --reload
#
# Example requests:
#   POST http://127.0.0.1:8000/play
#   Body: {"user_choice": "rock"}
#
#   POST http://127.0.0.1:8000/rock
#   (no body needed)
#
# The response will be JSON like:
#   {"user_choice": "rock", "computer_choice": "scissors", "result": "win"}
