
build_image:
	@docker build -t website:production .

website:
	@docker run --rm -p 0.0.0.0:5000:5000 -v $(shell pwd)/app:/home/website/app\
 										  -v $(shell pwd)/migrations:/home/website/migrations\
 										  -w /home/website/app website:production flask run\
	 									  -h 0.0.0.0