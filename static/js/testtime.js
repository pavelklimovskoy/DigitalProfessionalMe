function createTimeline (){
    test = null;

    // create a network
    let testContainer = document.getElementById('testing');

    // create some nodes
    let width = testing.clientWidth;

    let nodes = [
    {id: 1, x: 0, y: 1, label: 'Start', color: 'green', shape: 'circle'},
    {id: 2, label: 'Step 2', shape: 'square'},
    {id: 3, label: 'Step 3', shape: 'square'},
    {id: 4, label: 'Step 4', shape: 'square'},
    {id: 5, label: 'Step 5', shape: 'square'},
    {id: 6, label: 'Step 6', shape: 'square'},
    {id: 7, label: 'Step 7', shape: 'square'},
    {id: 8, label: 'Step 8', shape: 'square'},
    {id: 9, label: 'Step 9', shape: 'square'},
    {id: 10, label: 'Step 10', shape: 'square'},
    {id: 11, label: 'Step 11', shape: 'square'},
    {id: 12, x: width * 2, y: 1, label: 'Success!', shape: 'circle'}
    ];

    // create some edges
    let edges = [
    {from: 1, to: 2, style: 'arrow', color: 'red', width: 1, length: 200}, // individual length definition is possible
    {from: 2, to: 3, style: 'arrow', width: 1, length: 200},
    {from: 3, to: 4, style: 'arrow', width: 1, length: 200},
    {from: 4, to: 5, style: 'arrow', width: 1, length: 200},
    {from: 5, to: 6, style: 'arrow', width: 1, length: 200},
    {from: 6, to: 7, style: 'arrow', width: 1, length: 200},
    {from: 7, to: 8, style: 'arrow', width: 1, length: 200},
    {from: 8, to: 9, style: 'arrow', width: 1, length: 200},
    {from: 9, to: 10, style: 'arrow', width: 1, length: 200},
    {from: 10, to: 11, style: 'arrow', width: 1, length: 200},
    {from: 11, to: 12, style: 'arrow', width: 1, length: 200}
    ];

    let testData = {
    nodes: nodes,
    edges: edges
    };
    let testOptions = {
            width: '100%'
    };
    let test = new vis.Network(testContainer, testData, testOptions);
}