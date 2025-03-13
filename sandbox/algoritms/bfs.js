const isSeller = (person) => {
    // Function checking if a given person is a seller (condition to meet)
    return person.endsWith("m"); // Example condition - can be adjusted
  };
  
  const search = (name, graph) => {
    // We create a queue to store people to check
    const searchQueue = [...graph[name]];
    
    // We create a list of searched people to avoid cycles
    const searched = [];
  
    while (searchQueue.length > 0) {
      const person = searchQueue.shift(); // We get the first person from the queue
      
      // We check if the person has not been searched yet
      if (!searched.includes(person)) {
        // We check if the person is a seller
        if (isSeller(person)) {
          console.log(`${person} sells mangoes!`);
          return true;
        } else {
          // We add the person's friends to the queue
          searchQueue.push(...graph[person]);
          // We mark this person as searched
          searched.push(person);
        }
      }
    }
  
    return false; // Returns false if no seller is found
  };
  
  // Example graph
  const graph = {
    "ty": ["alice", "bob", "claire"],
    "alice": ["peggy"],
    "bob": ["anuj", "peggy"],
    "claire": ["thom", "jonny"],
    "anuj": [],
    "peggy": [],
    "thom": [],
    "jonny": []
  };
  
  // Running the search
  search("ty", graph);
  