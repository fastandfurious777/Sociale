async function GetBikes(){
  const response = await fetch("/map/get-bike-positions/");
  const responseData = await response.json();
  return responseData.bikes
}
async function AddMarker(bike){
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
  const marker = new AdvancedMarkerElement({
    map,
    position: { lat: bike.lat, lng: bike.lon },
  });     
  markers.push(
    {
      bike_id: bike.id,
      "marker" : marker,
    });
}

async function SetMarkers(){
  //Current bike list
  const bikes = await GetBikes();
  const getBikesIdList = () =>{
    let bikes_id = [];
    for (let bike of bikes){
      bikes_id.push(bike.id);
    }
    return bikes_id;
  };
  const getMarkersIdList = () =>{
    let ids = [];
    for (let marker of markers){
      ids.push(marker.bike_id);
    }
    return ids;
  };
  const bikesIds = new Set(getBikesIdList());
  const markerIds = new Set(getMarkersIdList());

  for (let bike of bikes){
    if (markerIds.has(bike.id)){
      continue; // All good the bike is displayed
    } else{
      await AddMarker(bike);
    }
  }

  for (let i = markers.length - 1; i >= 0; i--) {
    const marker = markers[i];
    if (bikesIds.has(marker.bike_id)) {
      console.log("success");
    } else {
      //Delete marker
      marker.marker.setMap(null);
      //Using splice we can adjust the size of array to the current number of bikes
      markers.splice(i, 1);
    }
  }
}
(g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})({
    key: "AIzaSyDqaEmMUlCcnwrTtVb0e467mhQryaPAJTI",
    v: "weekly",
    // Use the 'v' parameter to indicate the version to use (weekly, beta, alpha, etc.).
    // Add other bootstrap parameters as needed, using camel case.
  });
  let map;
  const markers = []

  async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");
  //const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  map = new Map(document.getElementById("map"), {
      center: { lat: 50.063481, lng: 19.932906 },
      zoom: 19,
      disableDefaultUI: true,
      mapId: 'f203d7d130752d37'});

  await SetMarkers();
  setInterval(SetMarkers, 10000);
}

