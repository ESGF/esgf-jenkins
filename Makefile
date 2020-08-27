.PHONY: get_repo build_assets

SHELL = /bin/bash

workdir ?= $(PWD)/workdir
repo_name = $(shell basename $(repo))


upload_script = $(PWD)/scripts/upload_github_release_asset.bash
repo_dir = $(workdir)/$(repo_name)
dist_dir = $(repo_dir)/dist

#
# make build_assets workdir=$WORKDIR branch=$BRANCH repo=$REPO_URL tag=<tag> ant_cmd=<ant_cmd_path> java_home=$JAVA_HOME

#

# $(shell echo repo $(repo))
# $(shell echo repo_name $(repo_name))

# make build_assets workdir=$WORKDIR branch=fix_build repo=https://github.com/esgf/esg-search tag=v4.18.2 ant_cmd=/var/lib/jenkins/work/misc/apache-ant-1.10.5/bin/ant java_home=/usr/local/java
# make publish_local workdir=$WORKDIR branch=fix_build repo=https://github.com/esgf/esg-search tag=v4.18.2 ant_cmd=/var/lib/jenkins/work/misc/apache-ant-1.10.5/bin/ant java_home=/usr/local/java


get_repo:
	mkdir -p $(workdir)
	git clone -b $(branch) $(repo) $(workdir)/$(repo_name)
	cd $(workdir)/$(repo_name) && git checkout tags/$(tag)


build_assets: get_repo
	cd $(workdir)/$(repo_name) && \
	export JAVA_HOME=$(java_home) && \
	$(ant_cmd) -Dversion_num=$(tag) make_dist

publish_local:
	cd $(workdir)/$(repo_name) && \
	export JAVA_HOME=$(java_home) && \
	$(ant_cmd) publish_local

upload:
	@for f in $(shell ls $(dist_dir)); \
		do echo ...uploading $${f}; \
		bash $(upload_script) github_api_token=$(token) owner=$(owner) tag=$(tag) repo=$(repo_name) filename=$(dist_dir)/$${f}; \
		sleep 10; \
	done

clean:
	[[ -d $(workdir) ]] && [[ -d $(workdir)/$(repo_name) ]] && \
	echo "removing $(workdir)/$(repo_name)" && \
	rm -rf $(workdir)/$(repo_name)


