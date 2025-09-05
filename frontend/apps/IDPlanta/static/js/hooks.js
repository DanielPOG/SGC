function useState(initValue){
  let value = initValue
  function get(){return value};
  function set(newValue){
    const prevType = typeof initValue
    const newType = typeof newValue
    if(prevType !== newType){
      console.error(`useState Exception: El nuevo tipo de dato debe ser ${prevType}`)
      return
    }
    value = newValue
    console.log('State cambiado', value)
  }
  return [get, set]
}

export default 
  useState
