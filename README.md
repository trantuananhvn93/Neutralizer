# Neutralizer

HOW TO
 All results generated for the project can be regenerated by running run_all.sh from within ./Code

 The final product of this script are javascript variables saved in ./Results/javascript
 To display the results as in ./Website/*.html it is necessary to change the folling line in the head of the HTML file.

      <!-- Show clustering of articles   -->
    <script src="../../Results/javascript/cluster80/topic1_top5_after_cb.js" ></script>


 This was used instead of JSON as modern browsers prohibit using JSON files offline for security reasons.
 The code for the reference mapper must also be added manually. 