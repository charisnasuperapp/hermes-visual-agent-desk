(function (root) {
  'use strict';

  // Coordinates match the 1280 × 720 office map. Doors are the gaps between walls.
  const walls = [
    [274, 0, 292, 375], [548, 0, 566, 250], [808, 0, 826, 265],
    [548, 284, 810, 302], [548, 302, 566, 427], [798, 302, 816, 427],
    [0, 451, 548, 469], [900, 451, 1280, 469],
    [898, 469, 916, 510], [898, 568, 916, 720]
  ];
  const furniture = [
    [70, 255, 225, 375], [645, 315, 795, 395],
    [900, 260, 1045, 345], [955, 580, 1220, 665],
    [635, 80, 785, 210], [1165, 120, 1250, 250]
  ];
  const obstacles = walls.concat(furniture);
  const nodes = {
    EXEC: [180, 405], EXEC_EXIT: [250, 420], WEST_HALL: [315, 420],
    LIBRARY: [405, 390], LIB_EXIT: [520, 435], HUB_W: [590, 445],
    HUB_M: [715, 455], HUB_E: [850, 440], LOUNGE: [610, 390],
    SERVER_A: [650, 235], SERVER_B: [750, 235], SERVER_RIGHT: [785, 277],
    KITCHEN_GATE: [838, 280], KITCHEN_TOP: [838, 235],
    KITCHEN_SOUTH: [850, 405],
    COFFEE: [975, 245], DINING_SOUTH: [1065, 400],
    ARCADE: [1190, 275], BOARD_OUT: [875, 535], BOARD_IN: [935, 535],
    BOARD_1: [970, 545], BOARD_2: [1035, 545],
    BOARD_3: [1100, 545], BOARD_4: [1165, 545],
    DORM_OUT: [570, 510], DORM_IN: [520, 510], DORM_AISLE: [520, 610],
    DORM_BOTTOM_RIGHT: [520, 685], DORM_LEFT: [175, 685],
    DORM_LEFT_TOP: [175, 565],
    BED_1: [480, 565], BED_2: [480, 645],
    BED_3: [190, 565], BED_4: [190, 645]
  };
  const links = [
    ['EXEC','EXEC_EXIT'], ['EXEC_EXIT','WEST_HALL'],
    ['WEST_HALL','LIBRARY'], ['LIBRARY','LIB_EXIT'],
    ['LIB_EXIT','HUB_W'], ['HUB_W','HUB_M'], ['HUB_M','HUB_E'],
    ['HUB_W','LOUNGE'], ['HUB_E','KITCHEN_SOUTH'],
    ['SERVER_A','SERVER_B'], ['SERVER_B','SERVER_RIGHT'],
    ['SERVER_RIGHT','KITCHEN_GATE'], ['KITCHEN_GATE','KITCHEN_SOUTH'],
    ['KITCHEN_GATE','KITCHEN_TOP'], ['KITCHEN_TOP','COFFEE'],
    ['KITCHEN_SOUTH','DINING_SOUTH'], ['DINING_SOUTH','ARCADE'],
    ['HUB_E','BOARD_OUT'], ['BOARD_OUT','BOARD_IN'],
    ['BOARD_IN','BOARD_1'], ['BOARD_1','BOARD_2'],
    ['BOARD_2','BOARD_3'], ['BOARD_3','BOARD_4'],
    ['HUB_W','DORM_OUT'], ['DORM_OUT','DORM_IN'],
    ['DORM_IN','DORM_AISLE'], ['DORM_AISLE','BED_1'],
    ['DORM_AISLE','BED_2'], ['DORM_AISLE','DORM_BOTTOM_RIGHT'],
    ['DORM_BOTTOM_RIGHT','DORM_LEFT'],
    ['DORM_LEFT','DORM_LEFT_TOP'], ['DORM_LEFT_TOP','BED_3'],
    ['DORM_LEFT','BED_4']
  ];

  function inside(x, y, r) {
    return x >= r[0] - 5 && x <= r[2] + 5 && y >= r[1] - 5 && y <= r[3] + 5;
  }
  function clear(a, b) {
    const distance = Math.hypot(b.x - a.x, b.y - a.y);
    const steps = Math.max(1, Math.ceil(distance / 5));
    for (let i = 0; i <= steps; i++) {
      const t = i / steps;
      const x = a.x + (b.x - a.x) * t;
      const y = a.y + (b.y - a.y) * t;
      if (x < 12 || x > 1268 || y < 12 || y > 708) return false;
      if (obstacles.some(r => inside(x, y, r))) return false;
    }
    return true;
  }
  function point(key) { return { x: nodes[key][0], y: nodes[key][1] }; }
  function nearestVisible(pos) {
    return Object.keys(nodes).filter(k => clear(pos, point(k)))
      .sort((a,b) => Math.hypot(pos.x-nodes[a][0],pos.y-nodes[a][1]) -
                     Math.hypot(pos.x-nodes[b][0],pos.y-nodes[b][1]))[0];
  }
  function path(startX, startY, endX, endY) {
    const start = {x:startX,y:startY}, end = {x:endX,y:endY};
    if (Math.hypot(endX-startX,endY-startY) < 90 && clear(start,end)) return [end];
    const first = nearestVisible(start), last = nearestVisible(end);
    if (!first || !last) return [];
    const queue = [first], previous = {[first]:null};
    while (queue.length && !(last in previous)) {
      const here = queue.shift();
      for (const [a,b] of links) {
        const next = a === here ? b : b === here ? a : null;
        if (!next || next in previous || !clear(point(here),point(next))) continue;
        previous[next] = here;
        queue.push(next);
      }
    }
    if (!(last in previous)) return [];
    const route = [];
    for (let at = last; at; at = previous[at]) route.unshift(point(at));
    if (Math.hypot(start.x-route[0].x,start.y-route[0].y) < 4) route.shift();
    if (!route.length || Math.hypot(route[route.length-1].x-end.x,route[route.length-1].y-end.y) > 4) route.push(end);
    return route;
  }

  const api = { path, clear, nodes, links, walls, furniture };
  root.OfficeNavigation = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(typeof window !== 'undefined' ? window : globalThis);
