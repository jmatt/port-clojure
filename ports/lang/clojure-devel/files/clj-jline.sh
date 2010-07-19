#!/bin/sh

# clj - Clojure launcher script


cljjar='lib/clojure.jar'
cljclass='clojure.main'
jlineclass='jline.ConsoleRunner'

dir=$0
while [ -h "$dir" ]; do
  ls=`ls -ld "$dir"`
  link=`expr "$ls" : '.*-> \(.*\)$'`

  if expr "$link" : '/.*' > /dev/null; then
    dir="$link"
  else
    dir=`dirname "$dir"`"/$link"
  fi
done

dir=`dirname $dir`
dir=`cd "$dir" > /dev/null && pwd`
cljjar="$dir/../$cljjar"
jlinejar="$dir/../../jline.jar"
cp="${PWD}:${jlinejar}:${cljjar}"

# Add extra jars as specified by `.clojure` file
# Borrowed from <http://github.com/mreid/clojure-framework>
if [ -f .clojure ]; then
  cp=$cp:`cat .clojure`
else
  # Default to ~/.clojure if no .clojure is found.
  if [ -f $HOME/.clojure ]; then
    cp=$cp:`cat ~/.clojure`
  fi
fi

# .clojure.clj is the init file
if [ -f .clojure.clj ]; then
  cljinit="-i .clojure.clj"
else
  # Default to ~/.clojure.clj if no .clojure.clj is found in the current working directory
  if [ -f $HOME/.clojure.clj ]; then
    cljinit="-i ${HOME}/.clojure.clj"
  else
    cljinit=""
  fi
fi

if [ -z "$1" ]; then
  exec java -classpath $cp $jlineclass $cljclass $cljinit --repl
else
  scriptname=$1
  exec java -classpath "$cp" $jlineclass $cljclass $cljinit $scriptname -- "$@"
fi
