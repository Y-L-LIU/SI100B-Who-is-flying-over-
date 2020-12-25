# SI 100B Project: Who is Flying over? - Week 3

* **Code and Report Due**: 10:00 am, December 25th, 2020, China Standard Time 
* **Face to Face Check**: From 10:15 am, December 25th, 2020, China Standard Time at SIST 1A-109

From this week on, this project will be divided into two parallel parts. The two parallel sub-projects will require you to finish the same set of functionalities for your crawler and LED controller. However, those two parallel sub-projects, namely easy and advanced, are based on different technology stack thus have different difficulty. You are only required to finish one of them. The advanced sub-project prepares you for task 4’s 10-point bonus option (4 points for the other option) which is also based on a mini website.

In this week, you are building a web interface for controlling how your crawler and LED behave. Essentially, you are required to write a simple interface for your user, which allows them to change the behavior of your crawler and LEDs.

## Easy: Building Command Line Interface

The most straightforward way to build a control panel for a beginner is to build a Command Line Interface (CLI). You should have already used some sort of CLIs in SI100B which as the shell on your computer and the interactive Python interpreter. The easy level of the project require you to build a simple CLI that could change the behavior of your crawler and LEDs.

A simplest CLI program works as follows: it first prints out a prompt (命令提示符) asking the user to input a command. After the user submits the command with `enter`, the command is parsed by the program and executed. The result of the command is then printed out. Finally, another prompt is printed out, asking the user for a new input.

Read the description above, open a real CLI program (e.g., the interactive Python interpreter), and explore how it works. Answer the following questions:

- How can you get input from the user? What functions can you utilize in Python?
- How can you feed back the result to the user?

Let's get down to implement the controller in function `_main()` of `cli/cli.py`.

Your program should be able to control the following parameters of your crawler and LED:

- The central coordinate and the northeastern corner's coordinate of the data that the crawler is going to crawl;
- The frequency of fetching data from the FlightRadar24/FlightAware ;
- The way how your LED works. For example, change among different schemes of working or simply change the frequency of how it blinks.

You need to design a working scheme of how to represent each one of the parameters in your CLI. For example, in our design, we use `set coord 30 104` to ask the program to change the central coordinates to 30N,104E. You can design your own way of representing each of the commands in your program. You should also include a command in your program to display all the parameters currently in use.

**Hint on implementation**: You may have noticed that the program you are currently writing works independently from your crawler and LED controller. There is no direct way of communicating between them. You should come up with a way to pass on the parameters' change among the CLI program, your crawler and the LED controller. Following are some possible ways (in the increasing order of difficulty):

- Use a file. Serialize the parameters to a universal format (like JSON)and store it somewhere in the file system. Let the crawler to check the parameter change in the file periodically;
- Use the IPC primitives provided by the Python `multiprocessing` module. Read `main.py` and try to understand how it create two processes. Then read the documentation of the `multiprocessing` module. You can figure out what primitive to use and how to use it;
- Use the UNIX socket. You can also use the UNIX domain socket provided by Linux. Refer to the manual page and some kind of system programming guide if you want to try this approach;
- Use some kind of key-value store mechanism. This is a totally overkill for this project. However, many large-scale projects will use this approach. This requires you to set up some kind of key-value store database like `redis` on your machine and use it for data transferring.

Test your CLI by running `main.py` directly. `main.py` will start your crawler, your LED controller and this CLI for you.

Following is how our CLI program outputs:

```bash
>>> set coord 30 104
Coodinate: 30.0, 104.0
>>> set range 100
Range: 100 nm
>>> show coord
Coodinate: 30.0, 104.0
```

## Advanced: Building Web Server

Choosing this advanced option requires you to learn some basics of web development through online reading. Web development can be complicated. In this project, you are only required to implement simplest functionalities with handy tools like Flask.

You will write a simple web control panel for your crawler. For the web server, we are using a lightweight web framework called Flask. Your Pi should have Flask installed already.  If it is not installed, run `pip3 install flask` in your terminal.

First, read the [documentation](https://flask.palletsprojects.com/en/1.1.x/) of Flask. Learn how to do the following things:

- How to serve the request sent from the client for a specific path? For example, if a request is requesting the path `/public` on your server and another one is requesting `/confidential` on your server, how could you distinguish them and send different responses?
- How to serve different request methods? For example, one request is sent to your server for the path `/public` with a `GET` method and another one with a `POST` method, how could you distinguish them and send different responses?
- How to render a HTML template in Flask? How to create a simple template in Flask?
- How to get the form data the user sent to your server in a `POST` request? Which data type is it?

Then read this [documentation](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Getting_started), this [documentation](https://developer.mozilla.org/en-US/docs/Learn/Forms/Your_first_form) and other online resources. Learn how to do the following:

- How to specify the title of a web page? How to add a paragraph to a web page? How to add a title to a web page?
- How to design a form on a web page? How to add text box to your form? How to add an option to your form?
- How to send the content of the form to the server? What HTTP methods are generally used for those requests? In Flask, how will you handle the request containing a form?

Prepare your answers in your project report for this week.

Let’s get down to the real work. You are filling the `web_server/server.py` file and its framework  is provided. The script is already good for run except that you will get an HTTP `500` error every time you access a page on it. You can run it by `python3 web_server/server.py` and open the page it serves by opening `http://<pi-ip>:8999` in your browser. Walk through the script, and make sure you understand the meaning of each part of it.

Then, you need to implement the control panel at `http://<pi-ip>:8999/config`. The control panel should support changing the following parameters:

- The central coordinate and the northeastern corner's coordinate of the data that the crawler is going to crawl;
- The frequency of fetching data from the FlightRadar24/FlightAware ;
- The way how your LED works. For example, change among different schemes of working or simply change the frequency of how it blinks.

Your control panel should display the parameters currently in use to the visitor and present a simple form for the user to change the parameters. Changes should be reflected on the behavior of the LED and crawler next time you fetch data from FlightRadar24/FlightAware. You need to think about how to transmit the changed parameters to the crawler (hint below) and which part of your crawler should be changed.

Once you finish your implementation, run `python3 main.py`, verify if your server works and whether the changes in those parameters will influence the behavior of your crawler and LEDs.

**Hint on implementation**: You may have noticed that the program you are currently writing works independently from your crawler and LED controller. There is no direct way of communicating between them. You should come up with a way to pass on the parameters' change among the CLI program, your crawler and the LED controller. Following are some possible ways (in the increasing order of difficulty):

- Use a file. Serialize the parameters to a universal format (like JSON)and store it somewhere in the file system. Let the crawler to check the parameter change in the file periodically;
- Use the IPC primitives provided by the Python `multiprocessing` module. Read `main.py` and try to understand how it create two processes. Then read the documentation of the `multiprocessing` module. You can figure out what primitive to use and how to use it;
- Use the UNIX socket. You can also use the UNIX domain socket provided by Linux. Refer to the manual page and some kind of system programming guide if you want to try this approach;
- Use some kind of key-value store mechanism. This is a totally overkill for this project. However, many large-scale projects will use this approach. This requires you to set up some kind of key-value store database like `redis` on your machine and use it for data transferring.

You are required to explain the approach you take (can be other than the ones above)  to the TA.

## Submission

You should submit a report on how you design this part of the project and also your code.

Submit your report as a PDF file to Gradescope. Submit your implementation code to GitLab by creating a tag as followed. Attend the face to face check at SIST 1A-109. You are allowed to submit your report and implementaion for unlimited times before the deadline, only the last submission will be used for grading but all your code in to the code base and all the versions of your report are subject to the [academic code of conduct](https://si100b.org/resource-policy/#policies).

First, make a commit from your files. From the root folder of this repository, run

```shell
git add .
git commit -m '{your commit message}'
```

Then add a tag to create a submission.

```shell
git tag {tagname} && git push origin {tagname}
```

You need to define your own submission tag by changing `{tagname}`, e.g.

```shell
git tag first_trial && git push origin first_trial
```

**Please use a new tag for every new submission.**

Every submission will create a new GitLab issue, where you can track the progress.