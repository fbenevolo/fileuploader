compose-build:
	sudo docker compose down
	sudo docker compose build
	sudo docker compose up

tf-and-seed:
	cd terraform && terraform plan && terraform apply
	backend/venv/bin/python backend/src/scripts/seed.py

tf-destroy:
	cd terraform && terraform destroy