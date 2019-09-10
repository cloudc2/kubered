<p align="center">
	<img src="logo/kuberedlogoTxt.png" width="40%" align="center" alt="Kubered">
</p>

# Kubered

V 0.1

Kubered is a script used to deploy C2 infrastructures using Kubernetes.

## Dependencies

Kubered needs the following programs installed in order to run
* awscli
* kubectl
* kops
* tiller

## Notes

This is an early alpha, it works but it's not pretty.
You will need to compose your own docker image for cobalt strike by using the file in /dockerfiles/teamserver/Dockerfile, then upload it to a private Docker Repo. This is because you need a valid cobalt strike license to download it. It will automate this in the next release.

You will need to edit the config.json file before you run kubered.py, you also need to have configured the awscli and have appriate AWS permissions on your aws account to deploy 
