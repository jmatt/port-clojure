(if (find-ns 'clojure.contrib.repl-utils)
    (use 'clojure.contrib.repl-utils))

(defn exit [& {:keys [statuscode] :or {statuscode 0}}]
      (System/exit statuscode))

(def *classpath* (System/getProperty "java.class.path"))