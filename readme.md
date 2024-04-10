# Liine Take Home

Hi! I'm your first Markdown file in **StackEdit**. If you want to learn about StackEdit, you can read me. If you want to play with Markdown, you can edit me. Once you have finished with me, you can create new files by opening the **file explorer** on the left corner of the navigation bar.

# Loading the Data

1. Initialize an empty list for each day of the week
2. For each row/restaurant, parse its days of the week, then add it to the day of the week list as an object with the form:
   {
   name,
   serialized time
   }

    Note: if the times are not listed, append a \* to the name.

3. From the lists, build an interval tree for each day of the week. We are using a simplified tree without any insert/delete method. For that reason, we need to sort the lists in such a way that allows the tree to be built correctly without modification.
