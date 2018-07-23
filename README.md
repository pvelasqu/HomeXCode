# HomeX Back-End Test

Hey! Seems you are interested in working at HomeX. This isn't a timed test, take as much or as little time as you feel you need (unfortunately we do need this back to assess you, so do keep that in mind). 

This is our little test to see what you know, and how you apply your knowledge to a real life use case. The solution you will build as part of this test is very similar to solutions we would use in our application at HomeX. We feel it is best to give you a test that will accurately reflect your ability to work within our team and on the specific features we develop.

## The Test

You will be given a MySQL 5.7 database script with 2 tables relating to activities. The first table is a list of activities and the hierarchy of those activities. The second one gives the id of people working on each activity. The table structures are provided below for a description of the activities. 

| activities |
|:----------:|
| **id** _int_ (PK)    |
| **name** _varchar(40)_|
| **parent_activity_id** _int_ _NULLABLE_ |

| activities_people |
|:-----------------:|
| **id** _int_ (PK) |
| **activity_id** _int_ (FK) |
| **person_id** _int_ |

You will also have an api endpoint that takes in an id and returns a person's name.
`GET http://interview.homex.io/api/people/{person_id}`

RESPONSE
```
{
  "name" : "John Doe"
}
```


In this test, you have to create an application that prints out the hierarchy of the activity tree, and next to each activity lists the names of the people working on that activity.

For example, a solution could be a console app that prints something like the following:
```
Develop Software
    Architecture - Marlene Reed, Cindy Holland, Warren Christensen
        Security Design - Cindy Holland, Warren Christensen
        Technical Design - Marlene Reed, Warren Christensen
    Development - Phyllis Joseph, Anna Miles, Jessie Dunn, Cindy Holland, Warren Christensen
        Coding - Carrie Hunt, Anna Miles, Marlene Reed
        Infrastructure - Carrie Hunt, Phyllis Joseph, Jessie Dunn
        Testing - Carrie Hunt, Phyllis Joseph, Warren Christensen
    Product Design - Ethel Lambert, Hope Ruiz, Warren Christensen
        Business Requirements - Victoria Hogan, Nick Greer, Warren Christensen
            Customer Requests - Luis Park, Homer Carson, Nick Greer
            Legal Rules - Victoria Hogan, Mindy Fuller, Andrew Hawkins
        UX Design - Ethel Lambert, Rickey Hill, Mabel Nash
            Story Boarding - Rickey Hill, Elvirra Padilla, Jessie Dunn
            User Testing - Gerard Neal, Mabel Nash, Beatrice Elliot
```
Where each indent represents a new level down the tree.

## Guidelines

Here are some expectations for the final product that you build. 

**Coding Style**
- Keep it clean, write self commenting code where possible, otherwise add comments where not. 
- Code like you would if you were working on a real team production project.
- It doesn't have to be perfect (that's what PRs are for), but we want to see the quality you would normally put into your work.
- Keep it structured. What structure you use is up to you, but don't just throw everything in the Main method.

**What can I use?**

- Feel free to use any language/framework/library you feel is necessary. We are mostly a C# .Net shop for our backend, so if you can, preferably use that, but we won't hold it against you if you pick another language (if you feel more comfortable with that).
- If there are any special compile/run instructions, include those.

**Requirements**
- A tree of the activities as they're laid out in the database needs to be displayed (either as text or visually as a webpage)
- Next to/in each node of the tree, a list of the names of the people working on that activity needs to be displayed.

**Notes**
- assume the size of the tree can be large, but < 1,000,000 nodes.
- assume the number of people working on activities will be < 10,000.
- assume a node can have 0 to many people working on it.
- there is no requirement on the ordering of the nodes/names, just that they are in the tree in the parent child hierarchy.

**Cool Extras**
- output to an http endpoint (as JSON)
- render tree in HTML
- render tree with collapsible nodes in HTML
- assume the size of the tree can be arbitrary, e.g. 100,000,000,000 nodes.
- unit and integration tests

## Submission

To submit the test, ZIP up your project (including this README) and email it to [amanda@homex.com](mailto:amanda@homex.com).
Include any assumptions/comments on how you feel about the test.
