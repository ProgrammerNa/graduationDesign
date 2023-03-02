export const tree = (data:any) => {
  const tree = data.filter((father:any) => {
        const arr = data.filter((child:any) => {
          return father.id == child.parent_id
        })
        if (arr.length > 0) {
          father.children = arr
        }
        return father.parent == null
      })
    const treeData = tree.filter( (i:any) => i.parent_id === 0)
    return treeData
}

export const selectCascader = (data:any) => {
  const tree = data.filter((father:any) => {
        const arr = data.filter((child:any) => {
          return father.value == child.parent_id
        })
        if (arr.length > 0) {
          father.children = arr
        }
        return father.parent == null
      })
    const treeData = tree.filter( (i:any) => i.parent_id === 0)
    return treeData
}