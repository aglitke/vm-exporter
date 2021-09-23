# vm-exporter
This repository provides an example workflow to export a KubeVirt VM to another cluster.  Starting with a powered off VM in the source cluster, a simple HTTP server is started to serve the disk image with xz compression.  The VM yaml is recreated on the target cluster with a slight change to import from the HTTP server on the source cluster instead of the original source.  The containerized-data-importer (CDI) will transfer and unpack the VM disk into the target cluster.

