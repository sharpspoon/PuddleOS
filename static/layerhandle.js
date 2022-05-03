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
                    <tr>
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
                    </tr>`;
    layerTableBody.innerHTML += newHTML
})