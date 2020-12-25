# SI 100B Project: Who is Flying over? - Week 4

* **Code and Report Due**: 10:00 am, December 30, 2020, China Standard Time 
* **Face to Face Check**: TBD

This week, we are going to visualize the data you crawled from FlightRadar24/FlightAware. Python provides a lot of useful tools for data processing and visualization. `numpy` and `matplotlib` are often used for these tasks. In this part, you are going to utilize those two tools to do data aggregation and display the result in plots on a web page on your web server in real time.

## Before You Start

Read the [documentation](https://matplotlib.org/contents.html) of `matplotlib`, find out how to do the following things:

- How to create a plot?
- How to draw line graph (折线图), histogram (直方图), bar chart (条形图) and pie chart (饼状图)?
- How to change the legend, x-axis label and y-axis label of a graph?
- How to save the plot as an image?

**For students who want to finish the advanced project**, go back to the documentation of Flask, find out how to do the following things:

- How to serve image with Flask?
- How to add a route (that handles new URLs) to Flask?
- How to render an HTML template using Flask with parameters?

Write a simple program to plot the function $y= x^2$ (x from -1 to 1) with `matplotlib` and save the plot as a PNG-formatted image. Prepare to explain your answers to those questions and your simple program to TAs during check.

## Draw the Plots

### Plot

First you need to draw the plot. Remember that in task 1, we stored the data from FlightRadar24/FlightAware to a file on the file system, you may need to load the data from the file before you start to draw the plot.

In this project, you can choose your own way of interpreting the data and drawing your own plot. In task 1, you collected data from FlightRadar24/FlightAware, including the tail number, departure city, destination city, flight number and so on. You can choose some of them to do data aggregation and plot your own graph of the aggregated data. For example, you could explore the destination of the airplanes by plotting a bar chart counting numbers of flights for each destination. Come up with two ways of data aggregation and draw corresponding plots. Then try to implement them with `matplotlib` and `numpy`. Keep the questions above in your mind during implementation.

### Easy: Display Your Plot

This section is for students who want to finish the easy version of this sub-project.

The plots should update in real time with new data from FlightRadar24/FlightAware.

### Advanced: Display through Web Server

This section is for students who want to finish the advanced version of this sub-project.

Now you have your own way to display the data. Next, you need to display the plot to the users. Keep in mind that your plot should be updated in real time (i.e., after new data arrives from the crawler, the user should be able to see the graphs rendered from the new data once he/she refreshes the webpage). In this part, if you like, you can use tools other than matplotlib to do the visualization. For instance, you can use tools to create interactive visualizations.

Thinking about the following questions when you design your display page:

1. When do you update your graph? When the new data comes, or when the user request comes?

2. How do you store the data used for rendering the graph?

3. How do you store the graph after being rendered by `matplotlib`?

4. How can Flask read the graph you stored?

In `web_server/server.py`, continue implementing your web server in function `vis()`, so that the server could display both of the two graphs you created in the last step. To achieve this, you may need to return an HTML document to the browser that includes `<img>` tags (search for how to use it online) for the two graphs. Also, add an additional tag to your HTML document to make the page refreshed every 5 seconds to reflect the up-to-date data (search online for how to do so.).

Now start the project and visit `127.0.0.1:5000` in your browser to show your implementation.

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