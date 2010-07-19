#!/bin/sh

# clj - Clojure launcher script

BREAK_CHARS="\(\){}[],^%$#@\"\";:''|\\"

cljjar='lib/clojure.jar'
cljclass='clojure.main'
cljcompletions='.clj_completions'

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
cp="${PWD}:${cljjar}"
cljcompletions="$dir/../$cljcompletions"

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
  # Default to ~/.clojure.clj if no .clojure.clj is found
  if [ -f $HOME/.clojure.clj ]; then
    cljinit="-i ${HOME}/.clojure.clj"
  else
    cljinit=""
  fi
fi

if [ -z "$1" ]; then
  exec rlwrap -m '\' --remember -c -b $BREAK_CHARS -f $cljcompletions java -classpath "$cp" $cljclass $cljinit --repl
else
  scriptname=$1
  exec java -classpath "$cp" $cljclass $cljinit $scriptname -- "$@"
fi
