Feature 1: User updates sprint status
Scenario: the user as authority     
       Given: the sprint exist
    then:  the sprint status should be displayed
    And a task was added to the done cards
    And: the user can update status

Scenario: the user as authority     
        Given: the sprint exist
    then:  the sprint status should be displayed
    And a task was not added to the done cards
    And: the user cannot update status

Scenario: the user does not have authority     
       Given: the sprint exist
    Then:  the sprint status should not be displayed
    Then: the user can request authorization

Feature 2: User reports bug
    Scenario: a bug exists within the program
Given: the bug is high priority 
And: user files appropriate report
When: the bug is entered into the system
Then: the report and its priority level is logged 
And: the team is notified

Feature 3: User completes task
Given A current sprint is active
And the user has an active task
When The given task is completed
The user marks the task as done
And it is put into the completed tasks section

Feature 4: User re-activates a task
    Given A task has been completed
    When the user wants to change the status of a task
    The task is marked incomplete
    And is put into the section with the unfinished tasks

