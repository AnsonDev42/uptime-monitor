# uptime-monitor
[![Docker Image CI](https://github.com/AnsonDev42/uptime-monitor/actions/workflows/docker-image.yml/badge.svg)](https://github.com/AnsonDev42/uptime-monitor/actions/workflows/docker-image.yml) [![Pytest CI](https://github.com/AnsonDev42/uptime-monitor/actions/workflows/pytest-ci.yml/badge.svg)](https://github.com/AnsonDev42/uptime-monitor/actions/workflows/pytest-ci.yml)
---
This repo is the back-end implementation of the following project.
---

###  Demo
Click [here](https://uptime-monitor-front.pages.dev) to see for yourself

![image](https://github.com/AnsonDev42/uptime-monitor-front/assets/58594437/9a119264-49b8-4f08-9810-6198456b27ad)
![image](https://github.com/AnsonDev42/uptime-monitor-front/assets/58594437/308529f3-e8f4-4f96-85e6-f845e572c603)



---

### Running / Building PART1/2 (for front-end)
Installing Bun (the front-end package manager): https://bun.sh/
- Install dependencies(only need to run once) : `bun install`
- Run for development: `bun run dev`
- Build for production: `bun build`

Fork [frontend](https://github.com/AnsonDev42/uptime-monitor-front) and you can easily deploy it for free in [Cloudflare Page](https://pages.cloudflare.com/), [Vercel](https://vercel.com/) and etc.

---

### Running / Building PART2/2 Method1 **RECOMMENDED** (for backend-end)

Installing [Docker and Docker-compose](https://docs.docker.com/compose/install/)
- modify your configration in `docker-compose.yml` file if needed
- copy the `.env.dev` to `.env`, modify in `.env`
- docker-compose up

---

### Running / Building PART2/2: Method2 (for backend-end)
Installing [peotry](https://python-poetry.org/) (the back-end package manager for python):
- copy the `.env.dev` to `.env`, modify in `.env`
- Install dependencies(only need to run once) : `poetry install`
- Install and run both postgresDB **and** rabbitMQ
- In one shell to run Django Server: `./manage.py runserver`
- In another new shell to run celery server: `celery -A uptimemonitor worker --loglevel=INFO`
- In another new shell to run celery-beat: `celery -A uptimemonitor beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler`
  



---

### Objectives:
- a uptime dashboard ([Django-backend](https://github.com/AnsonDev42/uptime-monitor) + [NextJS-frontend(Client-Side-Render) in **TypeScript**](https://github.com/AnsonDev42/uptime-monitor-front)
- notify user when server is down and when server is restored


### Scope:
- support system services (smb, shairport)
- docker container monitoring
- database(postgres) monitoring
- periodic checks
- notification via email, bark, telegram
- web dashboard

### System Design:
![system-design.svg](docs%2Freadme-img%2Fsystem-design.svg)

### (oversimplified) Database Schema
![database-design.svg](docs%2Freadme-img%2Fdatabase-design.svg)
