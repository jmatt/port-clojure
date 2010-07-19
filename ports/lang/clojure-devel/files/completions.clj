#!/usr/bin/env clj
(def *completions-filename* ((apply hash-map *command-line-args*) "-o"))

(def completions (sort (reduce concat (map (fn [p] (keys (ns-publics (find-ns p)))) '(clojure.core clojure.java.io clojure.main clojure.pprint clojure.repl clojure.set clojure.xml clojure.zip)))))

;(defn writer []
;(if *completions-filename*
;(java.io.FileWriter. *completions-filename*)
;(java.io.OutputStreamWriter. System/out)))
;
;(with-open [f (java.io.BufferedWriter. (writer))]
;  (.write f (apply str (interleave completions (repeat "\n")))))

(with-open [f (java.io.BufferedWriter. (java.io.FileWriter. ".clj_completions"))]
    (.write f (apply str (interleave completions (repeat "\n")))))
