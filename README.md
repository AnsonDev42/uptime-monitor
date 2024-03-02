# uptime-monitor
This repo is the back end implementation of the following project.
### Objectives:
- a uptime dashboard ([Django-backend](https://github.com/AnsonDev42/uptime-monitor) + [NextJS-frontend(Client-Side-Render)](https://github.com/AnsonDev42/uptime-monitor-front)
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
