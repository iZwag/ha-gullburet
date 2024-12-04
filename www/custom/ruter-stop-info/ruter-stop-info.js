import {
  LitElement,
  html,
  css,
} from "https://cdn.jsdelivr.net/gh/lit/dist@2/core/lit-core.min.js";

const icons = {
  "mdi:bus":[0,0,32.0,32.0,"M11.625 22.812a2.188 2.188 0 1 1-2.188-2.188 2.188 2.188 0 0 1 2.188 2.188zM29.429 10H2.572a.574.574 0 0 0-.572.573v11.228a.575.575 0 0 0 .572.573h3.347a3.543 3.543 0 0 1 7.037 0h6.088a3.543 3.543 0 0 1 7.037 0h3.348a.575.575 0 0 0 .571-.573V10.574a.574.574 0 0 0-.57-.574zM8.848 17H3.259v-4.647h5.589zm6.632 0H9.892v-4.647h5.588zm6.641 0h-5.6v-4.647h5.6zm6.621 0h-5.59v-4.647h5.59zm-3.992 5.812a2.188 2.188 0 1 1-2.188-2.188 2.188 2.188 0 0 1 2.188 2.188z"],
  "mdi:subway":[0,0,32.0,32.0,"M10 11.39V9h12v2.39h-4.6v13.29h-2.85V11.39z M16 4A12 12 0 1 1 4 16 12 12 0 0 1 16 4m0-2a14 14 0 1 0 14 14A14 14 0 0 0 16 2z"],
  "mdi:tram":[0,0,32.0,32.0,"M2.998 24.007h26V26h-26zm26.953-6.324l-.54-2.417-.947-4.22-.13-.57a.634.634 0 0 0-.597-.476H16.229l2.543-2.227a.662.662 0 0 0-.025-1.021l-3.432-2.745h-2.151l4.115 3.289L14.189 10H4.26a.64.64 0 0 0-.6.477l-.529 2.368-1.007 4.485-.079.353a3.09 3.09 0 0 0 .39 2.081l1.059 1.5H7v.759a.985.985 0 0 0 .984.977h3.043a.983.983 0 0 0 .987-.977v-.759h7.995v.76a.985.985 0 0 0 .987.976h3.042a.985.985 0 0 0 .985-.977v-.759h3.48l1.057-1.5a3.076 3.076 0 0 0 .39-2.081zM9.013 17H3.505l.913-4.647h4.595zm6.498 0h-5.51v-4.647h5.51zm6.497 0h-5.51v-4.647h5.51zm.99 0v-4.647h4.58L28.49 17z"],
  "mdi:walk":[0,0,32.0,32.0,"M12.22 9.094a.841.841 0 0 0-.536.498l-2.16 5.196a.874.874 0 1 0 1.614.668l2.01-4.833 1.544-.515-2.139 5.581a2.385 2.385 0 0 0 .211 2.104L7.73 28.205a1.25 1.25 0 0 0 2.251 1.089l4.658-9.635 5.072 9.672a1.25 1.25 0 0 0 1.688.527l.014-.008a1.25 1.25 0 0 0 .513-1.68l-5.162-9.842 2.137-5.575.466 1.598a.82.82 0 0 0 .476.52l3.321 1.777a.874.874 0 1 0 .713-1.595l-2.948-1.578-1.216-4.179a2.451 2.451 0 0 0-3.038-1.669 2.393 2.393 0 0 0-.083.026zm7.187-7.093a2.5 2.5 0 1 1-2.5 2.5 2.5 2.5 0 0 1 2.5-2.5z"],
  "mdi:ferry":[0,0,32.0,32.0,"M26.116 21.374l-.246-.152a5.452 5.452 0 0 0-6.106 0 4.027 4.027 0 0 1-2.463.767 4.015 4.015 0 0 1-2.462-.767 5.14 5.14 0 0 0-3.055-.936 5.125 5.125 0 0 0-3.05.936 4.03 4.03 0 0 1-2.464.767 4.016 4.016 0 0 1-2.46-.767 6.286 6.286 0 0 0-1.423-.704L2 22.194a5.024 5.024 0 0 1 1.175.589 5.13 5.13 0 0 0 3.046.938 5.124 5.124 0 0 0 3.045-.938 3.992 3.992 0 0 1 2.452-.764 4.022 4.022 0 0 1 2.457.764 5.108 5.108 0 0 0 3.043.938 5.117 5.117 0 0 0 3.043-.938 4.325 4.325 0 0 1 4.91 0c.022.014.045.03.07.044zm-.449-6.676l-1.662-6.662c-.054-.182-.207-.252-.465-.252h-2.41l-.374-1.744a.449.449 0 0 0-.576-.265l-.005.002L17.45 6.93a.594.594 0 0 0-.447.664v2.123H6.987a.49.49 0 0 0-.46.45l-1.008 4.52H3.84a.428.428 0 0 0-.431.326l-.726 3.774a7.998 7.998 0 0 1 1.721.708 3.212 3.212 0 0 0 1.83.492 3.22 3.22 0 0 0 1.833-.492 7.167 7.167 0 0 1 3.684-.947 7.171 7.171 0 0 1 3.688.947 3.214 3.214 0 0 0 1.83.492 3.207 3.207 0 0 0 1.83-.492 7.188 7.188 0 0 1 3.69-.947 7.167 7.167 0 0 1 3.686.947l.272.14 3.197-4.347a.39.39 0 0 0-.376-.59zm-14.34 0H6.755l.508-2.394h4.065zm5.551 0h-4.64v-2.394h4.64zm.875 0v-2.394h4.6l.482 2.394z"],
  "mdi:train":[0,0,32.0,32.0,"M2 23h24v2H2zm26.981-7.87l-4.908-4.944a.758.758 0 0 0-.494-.186h-9.467l3.879-1.945c.402-.213.402-.547 0-.76L11.625 4H9l6.707 3.66-4.63 2.34H2v11h24.573a3.43 3.43 0 0 0 2.408-5.87zm-9.714-.346v-2.79h3.802l2.695 2.79z"]
}

class RuterStopInfo extends LitElement {
  static get properties() {
    return {
      hass: {},
      config: {},
      walkingDistance: {},
      showDepartures: {}
    };
  }

  render() {
    const platformA = this.hass.states[this.config.entities[0]]
    const platformB = this.hass.states[this.config.entities[1]]
    const platformAStyle = `background-color: ${getStopColor(platformA.attributes.icon)};`
    const platformBStyle = `background-color: ${getStopColor(platformB.attributes.icon)};`
    const departuresA= [];
    const departuresB= [];
    let field = "";
    let departureA = [];
    let departureB = [];
    
    departuresA.push({
      routeNumber: getRouteNumber(platformA.attributes.route),
      routeName: getRouteName(platformA.attributes.route),
      due: formatDueTime(platformA.state)
    });

    departuresA.push({
      routeNumber: getRouteNumber(platformA.attributes.next_route),
      routeName: getRouteName(platformA.attributes.next_route),
      due: platformA.attributes.next_due_in
    });

    departuresB.push({
      routeNumber: getRouteNumber(platformB.attributes.route),
      routeName: getRouteName(platformB.attributes.route),
      due: formatDueTime(platformB.state)
    });

    departuresB.push({
      routeNumber: getRouteNumber(platformB.attributes.next_route),
      routeName: getRouteName(platformB.attributes.next_route),
      due: platformB.attributes.next_due_in
    });

    // Handle potential extra departures above the two default
    for(let i = 3; i < 10; i++ ) {
      field = "departure_#" + i;

      if (this.config.show_departures <= 2) {
        break;
      }
      if (this.config.show_departures < i) {
        break;
      }
      
      if (!(field in platformA.attributes)) {
        break;	
      }

      departureA = extractDepartureInfo(platformA["attributes"][field])
      departureB = extractDepartureInfo(platformB["attributes"][field])

      departuresA.push({
        routeNumber: departureA[0],
        routeName: departureA[1],
        due: departureA[2]
      });

      departuresB.push({
        routeNumber: departureB[0],
        routeName: departureB[1],
        due: departureB[2]
      });
    }

    // <hr class="divider">

    return html`
    <ha-card>
      <div class="container">
        <div class="board-header">
          <div class="header-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32.0 32.0" width="32" height="32">
              <path style="fill: white; stroke: white;" d="${icons[platformA.attributes.icon][4]}" />
            </svg>
          </div>
          <span class="header-title">
            ${getStopName(platformA.attributes.friendly_name)}
          </span>
          <div class="header-walkdist"> 
            <div class="walkdist-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32.0 32.0" height="1.5rem">
                <path style="fill: white; stroke: white;" d="${icons["mdi:walk"][4]}"/>
              </svg>
            </div>
            <div class="walkdist-time">
              ${this.config.walkingDistance} min
            </div>
          </div>
        </div>
        <div class="departures">
          ${departuresA.map((row) => html`
          <div class="departure">
            <div class="route-number" style="${platformAStyle}">
              ${row.routeNumber}
            </div>
            <div class="route-name">
              ${row.routeName}
            </div>
            <div class="route-due">
              ${row.due}
            </div>
          </div>
          `)}
        </div>
        <div class="spacer">
        </div>
        <div class="departures">
          ${departuresB.map((row) => html`
          <div class="departure">
            <div class="route-number" style="${platformBStyle}">
              ${row.routeNumber}
            </div>
            <div class="route-name">
              ${row.routeName}
            </div>
            <div class="route-due">
              ${row.due}
            </div>
          </div>
          `)}
        </div>
      </div>
    </ha-card>
    `;
  }
  
  // The user supplied configuration. Throw an exception and Home Assistant
  // will render an error card.
  // User shall supply two entities, one for each platform (or direction)
  // TODO: User could also supply walking distance
  // Name of Stop will be pulled from the first entity
  setConfig(config) {
    if (!config.entities) {
      throw new Error("You need to define an entity");
    }
    this.config = {
      ...config,
      walkingDistance: config.walking_distance || 0,
      showDepartures: config.show_departures || 10,
    };
  }
  
    // The height of your card. Home Assistant uses this to automatically
    // distribute all cards over the available columns.
  getCardSize() {
      return 5;
  }

  static get styles() {
    return css`
      .container {
        display: flex;
        flex-direction: column;
        font-size: 18px;
        color: white;
        padding: 8px 12px 4px 12px;
      }
      .board-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
        padding: 4px 0;
      }
      .header-title {
        text-align: left;
        flex-grow: 4;
        font-weight: bold;
      }
      .header-walkdist {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 5px;
      }
      .walkdist-time {
        font-size: 0.9em;
        text-align: right;
        color: var(--secondary-text-color) 
      }
      .departures {
        display: flex;
        flex-direction: column;
        padding: 4px 0;
      }
      .departure {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 4px 0;
        gap: 8px;
      }
      .route-number {
        background-color: #E60000;
        color: white;
        border-radius: 8px;
        padding: 5px;
        font-weight: bold;
        font-size: 0.9em;
        height: 1.3em;
        width: 1.3em;
        text-align: center;
        line-height: 1.3em;
      }
      .route-name {
        flex-grow: 4;
        text-align: left;
        font-size: 0.8em;
      }
      .route-due {
        font-size: 0.9em;
        flex-grow: 1;
        text-align: right;
        color: var(--primary-text-color)
      }
      hr.divider {
        border-top: 1px solid white;
        width: 90%;
      }
      .spacer {
        height: 5px;
        width: 100%;
      }
    `;
  }
}

  // Extracts the Stop name from the Platform entity
  function getStopName(friendlyName) {
    const matchExp = /Ruter\s(.+)\sPlatform/;
    const matches = friendlyName.match(matchExp);
    if (!matches) {
      return friendlyName;
    }
    return matches[1];
  }

  function getRouteNumber(routeName) {
    const matchExp = /(^[A-Za-z0-9]+)\s/;
    const matches = routeName.match(matchExp);
    if (!matches) {
      return "";
    }
    return matches[1];
  }

  function getRouteName(routeName) {
    const matchExp = /\d+\w{0,1}\s(.+)/;
    const matches = routeName.match(matchExp);
    if (!matches) {
      return routeName;
    }
    return matches[1];
  }

  // Example-format:
  // 12:09 18 Storo-Grefsen st.
  function extractDepartureInfo(departure) {
    const matchExp = /(\d\d\:\d\d)\s([A-Za-z0-9]+)\s(.+)/;
    const matches = departure.match(matchExp);
    if (!matches) {
      return ["00", "", "--:--"];
    }
    return [matches[2], matches[3], matches[1]];
  }

  function isRuterLine(routeId) {
    const matchExp = /RUT\:Line/;
    const matches = routeId.match(matchExp);
    if (!matches) {
      return false;
    }
    return true;
  }

  function getStopColor(mdIcon) {
  
    switch(mdIcon) {
      case "mdi:bus":
        return "E60000"
      case "mdi:tram":
        return "#0B91EF"
      case "mdi:subway":
        return "#EC700C"
      case "mdi:train":
        return "#003087"
      case "mdi:ferry":
        return "#682C88"
      default:
        return "E60000"
    }
  }

function formatDueTime(dueTime) {
  if (dueTime === 0 || dueTime === "0") {
    return "nå"
  } else {
    return dueTime + " min"
  }
}

customElements.define('ruter-stop-info', RuterStopInfo);