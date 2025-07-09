fmt:
	prettier -w static/
	uv tool run black .

check:
	prettier --check static/
	uv tool run black --check .
	uv tool run ruff check

run:
	uv run uvicorn main:app --reload
