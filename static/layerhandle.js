const addLayerBtn = document.getElementById('addLayerBtn');
const layerTableBody = document.getElementById('layerTableBody');
const layerCount = document.getElementById('layerCount');

addLayerBtn.addEventListener('click', function () {
    layerCount.value = parseInt(layerCount.value) + 1;
    const i = layerTableBody.children.length+1;
    // from csstricks
    const randomColorHex = '#'+Math.floor(Math.random()*16777215).toString(16);
    const startingSize = 25;
    const clusteringMethodOptions = `<option value="Agglomerative Complete Linkage Hierarchical Clustering" selected>Agglomerative Complete Linkage Hierarchical Clustering</option>
            <option value="DBSCAN">DBSCAN</option>`
    const newHTML = `
                    <tr class="saveMenuItem">
                        <th scope="row">${i}</th>
                        <td>
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" role="switch"
                                        id="nodeDisplay${i}id" name="nodeDisplay${i}" checked>
                            </div>
                        </td>
                        <td>
                            <div class="input-group mb-3">
                                <select class="form-select" id="layer${i}ClusteringMethodId"
                                        name="layer${i}ClusteringMethod">
                                    ${clusteringMethodOptions}
                                </select>
                            </div>
                        </td>
                        <td>
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" role="switch"
                                        id="puddleDisplay${i}id" name="puddleDisplay${i}">
                            </div>
                        </td>
                        <td><input type="number" class="form-control" id="layer${i}id" name="layer${i}"
                                    aria-describedby="layer${i}Help"
                                    value=10
                                    data-bs-toggle="tooltip" data-bs-placement="top"
                                    title="NOTE: Changing the number of nodes will also randomize them."
                                    required></td>
                        <td><input type="color" class="form-control form-control-color" id="layer${i}colorid"
                                    name="colorInput${i}"
                                    value=${randomColorHex} title="Choose your color"></td>
                        <td><input type="number" class="form-control" id="layer${i}sizeid" name="layer${i}size"
                                    aria-describedby="layer1sizeHelp"
                                    value=${startingSize}
                                    required></td>
                        <td>
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" role="switch"
                                        id="randomizeLayer${i}id" name="randomizeLayer${i}">
                            </div>
                        </td>
                        <td><button type="button" class="btn btn-danger deleteLayerBtn" value=${i} id="deleteBtn${i}">X</button></td>
                    </tr>`;
    layerTableBody.innerHTML += newHTML
    bindDeletes();
})

function bindDeletes() {
    const deleteBtns = document.getElementsByClassName('deleteLayerBtn');
    for (let btn of deleteBtns) {
        btn.addEventListener('click', function () {
            layerCount.value = parseInt(layerCount.value) - 1;
            btn.parentElement.parentElement.remove();
            let saveMenuItems = document.getElementsByClassName('saveMenuItem');
            let i = btn.value;
            for (let item of saveMenuItems) {
                if (item.children[0].innerHTML > i) {
                    let curr_i = parseInt(item.children[0].innerHTML);
                    item.children[0].innerHTML = curr_i - 1;

                    let check = document.getElementById(`nodeDisplay${curr_i}id`)
                    check.id = `nodeDisplay${curr_i-1}id`;
                    check.name = `nodeDisplay${curr_i-1}`;

                    let clustering = document.getElementById(`layer${curr_i}ClusteringMethodId`)
                    clustering.id = `layer${curr_i-1}ClusteringMethodId`;
                    clustering.name = `layer${curr_i-1}ClusteringMethod`;

                    check = document.getElementById(`puddleDisplay${curr_i}id`)
                    check.id = `puddleDisplay${curr_i-1}id`;
                    check.name = `puddleDisplay${curr_i-1}`;

                    let nodes = document.getElementById(`layer${curr_i}id`)
                    nodes.id = `layer${curr_i-1}id`;
                    nodes.name = `layer${curr_i-1}`;
                    nodes.ariaRoleDescription = `layer${curr_i-1}Help`;

                    let color = document.getElementById(`layer${curr_i}colorid`)
                    color.id = `layer${curr_i-1}colorid`;
                    color.name = `colorInput${curr_i-1}`;

                    let size = document.getElementById(`layer${curr_i}sizeid`)
                    size.id = `layer${curr_i-1}sizeid`;
                    size.name = `layer${curr_i-1}size`;

                    let randomize = document.getElementById(`randomizeLayer${curr_i}id`)
                    randomize.id = `randomizeLayer${curr_i-1}id`;
                    randomize.name = `randomizeLayer${curr_i-1}`;

                    let inner_deleteBtn = document.getElementById(`deleteBtn${curr_i}`)
                    inner_deleteBtn.id = `deleteBtn${curr_i-1}`;
                    inner_deleteBtn.value = curr_i-1;
                }
            }
        })
    }
}

bindDeletes();