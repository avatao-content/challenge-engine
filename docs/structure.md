# Challenge directory structure

There are descriptor files for a challenge, you can see the right structure format below:  


(D) = for Docker challenges only  
[ ] = optional

    repository_name ------------------------ (DIR)
        controller (D) --------------------- (DIR)
        solvable (D) ----------------------- (DIR)
        [src] ------------------------------ (DIR)
        [downloads] ------------------------ (DIR)
        config.yml ------------------------- (FILE)
            version ------------------------ (ITEM)
            [flag] ------------------------- (ITEM)
            enable_flag_input -------------- (ITEM)
            crp_config (D) ----------------- (ITEM)
                controller ----------------- (ITEM)
                    capabilities ----------- (ITEM)
                    mem_limit_mb ----------- (ITEM)
                    ports ------------------ (ITEM)
                    read_only -------------- (ITEM)
                solvable ------------------- (ITEM)
                    capabilities ----------- (ITEM)
                    mem_limit_mb ----------- (ITEM)
                    ports ------------------ (ITEM)
                    read_only -------------- (ITEM)
            skills ------------------------- (ITEM)
            recommendations ---------------- (ITEM)
            owners ------------------------- (ITEM)
        [CHANGELOG] ------------------------ (FILE)
        [README.md] ------------------------ (FILE)
        [LICENSE] -------------------------- (FILE)

## Structure details

In this section we detail the directory structure of challenges. Under the [skeleton](https://github.com/avatao/challenge-engine/tree/master/skeleton) directory in this repository you can find example content for all the items below. Also, we have prepared various challenge templates for different challenge types (e.g., [c](templates/c), [c#](templates/csharp), [static](templates/file), [java](templates/java), [ssh](templates/ssh), [telnet](templates/telnet), [xss](templates/xss)) that you can fork and customize according to your needs. So the structure is the following:

- **controller** \[docker\]: The directory for controller should always exist for docker-based challenges. Place here the scripts to check submitted user solution if the flag is not static (e.g., dynamically generated upon container start). The files in this directory _won't_ be accessible for users.
- **solvable** \[docker\]: The directory for solvable exists for most of the docker-based challenges. Place here all your challenges files (e.g., flag.txt, your server, database files).
- **downloads** \[optional\]: Optionally, if you want to share challenge files (e.g., crackme, some components, source code) with users please place them here. These can be also relative symlinks which point to another file (e.g., a file in the _solvable_ directory) in the challenge repository. *IMPORTANT* This directory is mandatory for static challenges. 
- **src** \[optional\]: Place all the other source codes and source files of a challenge into this directory. No matter if you have already placed some of these files under the `solvable` or `downloads` directory, please also put them here to have everything in one place.
- **config.yml**: A well-formatted YAML file which contains all the configuration parameters of the challenge. These parameters are the following:
    - **version**: Version number of the config file.  Currently it is `v2.0.0`.
    - **flag** \[optional\]: If a docker challenge has static flag or the challenge itself is static then insert your flag here. In that case we won't need to start up a distinct container for solution checking. **IMPORTANT**: _However, you have to still create controller for docker-based challenges with the `test` function implemented. This way, we make sure that your challenge is working properly and can be solved._ 
    - **enable_flag_input**: Solution submission can happen in two ways. The first option is that the user submits a text (flag) in an input field on the platform. In this case please set it *true* to tell the platform to create an input field for the solution submission. The second option is when the solution checking works by checking the state changes (e.g., files created, configuration modified) inside the container the user is working on. For example, when the user solves a programming challenge and the controller executes multiple unit tests to accept their code. In that case please set it *false* as their source code is the solution.
    - **crp_config \[docker\]**: The configuration on how to run the containers can be set here
        - **controller**:        
            - **capabilities**: Place here the list of required linux/docker capabilities for the controller. Have only the minimal capability (CAP drop all by default), and add only those you really need.
             [Read more.](https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities) e.g.: \["SETGID","SETUID"\]
            - **ports**: A list containing strings in a style of 'port_number/protocol' for the controller it should be \['5555/controller'\] by default
            - **mem_limit**: The memory limit for the controller. This is a string that ends with a capital M for megabyte e.g.: '100M'
           (Maximum '999M')
        - **solvable**:
            - **capabilities**: Place here the list of required linux/docker capabilities for the solvable.
            - **ports**: A list containing strings in a style of 'port_number/protocol'
            - **mem_limit**: Same as the controller            
                ```
                available ports and protocols:
                    PORT/tcp
                    PORT/udp
                    8888/http
                    2222/ssh
                    PORT/ws            
                ```
- **README.md** [optional]: Any additional information that you would like to tell about the challenge. If the original challenge is licensed this should be the extended README.md of that challenge.
- **CHANGELOG** [optional]: If you modified an existing licensed challenge, please summarize what your changes were.
