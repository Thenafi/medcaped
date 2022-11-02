# Medcaped

Python selenium and bs4 script to scrape https://medex.com.bd and https://www.shajgoj.com/(bs4 only) website filtering language specific & health related data. This was only made for educational purpose.

The files are very unstructured. The steps to run are -

1.  Extract medicines page URL.(link_extract)
2.  Get the HTML page source (for bs4 script only)(html_extract)
3.  Extract the data (data_extract)

Future plane - make the readme great, make the code more stable - more clean - fix medex cwd - fix medxfaq inefficiency with html extraction + link extraction at the same time

Problem caused in shakal and oushadbarta -
SO when i try save the html files using the res.text() it results in encoding error. Because there so no proper encoding guide in the response header and messed up the encoding. The solution I went with is to read the response in bytes and then bs4 to write the html with proper encoding. Then I got the expected output.
