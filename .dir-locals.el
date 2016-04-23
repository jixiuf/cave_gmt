((python-mode
  (indent-tabs-mode . nil)
  (eval . (progn
            (setq jedi:environment-root (expand-file-name  "./virtual/" (locate-dominating-file default-directory "Makefile" )))
            (setq jedi:server-args  `("--virtual-env" ,(expand-file-name  "./virtual/" (locate-dominating-file default-directory "Makefile" ))
                                      "--virtual-env" ,(expand-file-name  "~/python/")
                                      "--virtual-env" "/System/Library/Frameworks/Python.framework/Versions/2.7/"
                                      "--sys-path" ,(expand-file-name  (expand-file-name  "./src/" (locate-dominating-file default-directory "Makefile" )))
                                      "--sys-path" ,(expand-file-name  (expand-file-name  "./src/db" (locate-dominating-file default-directory "Makefile" )))
                                      "--sys-path" "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7"
                                      "--sys-path" "."
))
            (setq exec-path (delete-dups  (cons  (expand-file-name  "./virtual/bin/" (locate-dominating-file default-directory "Makefile" )) exec-path)))
            (setenv "PATH" (concat  (expand-file-name "./virtual/bin/" (locate-dominating-file default-directory "Makefile" ) ) ":" (getenv "PATH") ))
            (setenv "PYTHONPATH"  (expand-file-name "./src/" (locate-dominating-file default-directory "Makefile" ) ))
            (setenv "PYTHONPATH"  (expand-file-name "./db/" (locate-dominating-file default-directory "Makefile" ) ))
            ))))

