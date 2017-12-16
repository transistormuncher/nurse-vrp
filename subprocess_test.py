import subprocess


# subprocess.call(['java', '-jar', 'hello.jar', "argument-1", "argument-2"])


# java -jar *.jar jetty.resourcebase=webapp config=config-example.properties datareader.file=slovakia-latest.osm.pbf
subprocess.call(['java', '-jar', 'graphhopper/graphhopper-web-0.9.0-with-dep.jar', "jetty.resourcebase=webapp", "config=graphhopper/config-example.properties", "datareader.file=graphhopper/slovakia-latest.osm.pbf"])