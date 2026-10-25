(() => {
  const list = document.querySelector('#equipment-list');
  if (!list) return;
  const initial = [
    { id: 'DEMO-101', name: 'Compact excavator', location: 'North yard / Bay A' },
    { id: 'DEMO-102', name: 'Wheel loader', location: 'North yard / Bay B' },
    { id: 'DEMO-103', name: 'Portable generator', location: 'North yard / Bay C' }
  ];
  let records, events, snapshot, downloadURL;
  const resolutions = ['Confirmed at listed location', 'Location corrected: North yard / Service area', 'Assigned for follow-up; excluded from verified inventory'];
  const addEvent = (message) => events.push({ sequence: events.length + 1, time: new Date().toISOString(), message });
  const makeButton = (label, action, id) => {
    const button = document.createElement('button');
    button.type = 'button'; button.textContent = label;
    button.dataset.action = action; button.dataset.id = id;
    button.setAttribute('aria-label', `${label} ${id}`);
    return button;
  };
  function render() {
    list.replaceChildren();
    records.forEach((record) => {
      const row = document.createElement('article'); row.className = 'equipment-row';
      const info = document.createElement('div');
      const heading = document.createElement('h3'); heading.textContent = record.name;
      const detail = document.createElement('p'); detail.textContent = `${record.id} / ${record.location}`;
      const status = document.createElement('span'); status.className = `record-status ${record.state}`;
      status.textContent = record.state === 'pending' ? 'Awaiting review' : record.state === 'flagged' ? 'Exception: location needs review' : record.state === 'verified' ? 'Verified at listed location' : `Resolved: ${record.decision}`;
      info.append(heading, detail, status); row.append(info);
      const actions = document.createElement('div'); actions.className = 'row-actions';
      if (!snapshot && record.state === 'pending') actions.append(makeButton('Verify', 'verify', record.id), makeButton('Flag location', 'flag', record.id));
      if (!snapshot && record.state === 'flagged') {
        const wrap = document.createElement('div'); wrap.className = 'resolution';
        const label = document.createElement('label'); label.htmlFor = `decision-${record.id}`; label.textContent = 'Record the review decision';
        const select = document.createElement('select'); select.id = label.htmlFor;
        const placeholder = new Option('Choose a resolution', ''); select.add(placeholder);
        resolutions.forEach(text => select.add(new Option(text, text)));
        const resolve = makeButton('Resolve exception', 'resolve', record.id); resolve.disabled = true;
        select.addEventListener('change', () => { resolve.disabled = !select.value; });
        wrap.append(label, select, resolve); actions.append(wrap);
      }
      row.append(actions); list.append(row);
    });
    const pending = records.filter(r => r.state === 'pending').length;
    const flagged = records.filter(r => r.state === 'flagged').length;
    const done = records.length - pending - flagged;
    document.querySelector('#review-progress').textContent = snapshot ? 'Snapshot created. Review locked.' : `${done} of ${records.length} reviewed / ${flagged} open exception${flagged === 1 ? '' : 's'}`;
    document.querySelector('#signoff').disabled = !!snapshot || pending > 0 || flagged > 0;
    document.querySelector('#signoff-help').textContent = snapshot ? 'Reset the demo to start a fresh review.' : flagged ? 'Resolve every exception before creating the snapshot.' : pending ? 'Review all three records before creating a snapshot.' : 'All records have a documented decision. Ready to create a snapshot.';
    ['review','resolve','snapshot'].forEach(stage => document.querySelector(`#step-${stage}`).removeAttribute('aria-current'));
    document.querySelector(`#step-${snapshot || (!pending && !flagged) ? 'snapshot' : flagged ? 'resolve' : 'review'}`).setAttribute('aria-current', 'step');
    const log = document.querySelector('#audit-log'); log.replaceChildren();
    events.forEach(event => { const li = document.createElement('li'); li.textContent = event.message; log.append(li); });
  }
  function reset() {
    if (downloadURL) URL.revokeObjectURL(downloadURL);
    downloadURL = null; snapshot = null; events = [];
    document.querySelector('#download-snapshot').removeAttribute('href');
    records = initial.map(record => ({ ...record, state: 'pending', decision: null }));
    addEvent('Sample campaign opened with three fictional equipment records.');
    document.querySelector('#snapshot').hidden = true; render();
  }
  list.addEventListener('click', event => {
    const button = event.target.closest('button[data-action]');
    if (!button || button.disabled || snapshot) return;
    const record = records.find(r => r.id === button.dataset.id);
    if (!record) return;
    if (button.dataset.action === 'verify' && record.state === 'pending') { record.state = 'verified'; addEvent(`${record.id}: verified at the listed location.`); }
    else if (button.dataset.action === 'flag' && record.state === 'pending') { record.state = 'flagged'; addEvent(`${record.id}: flagged for location review.`); }
    else if (button.dataset.action === 'resolve' && record.state === 'flagged') {
      const decision = document.querySelector(`#decision-${record.id}`).value;
      if (!resolutions.includes(decision)) return;
      if (decision === resolutions[1]) { record.sourceLocation = record.location; record.location = 'North yard / Service area'; }
      record.state = 'resolved'; record.decision = decision; addEvent(`${record.id}: ${decision}.`);
    } else return;
    render();
    const focus = list.querySelector(`#decision-${record.id}`) || list.querySelector('select') || list.querySelector('button:not(:disabled)') || document.querySelector('#signoff');
    focus.focus();
  });
  document.querySelector('#signoff').addEventListener('click', () => {
    if (snapshot || records.some(r => !['verified','resolved'].includes(r.state))) return;
    addEvent('Review snapshot created; records locked for this session.');
    snapshot = { demonstration: true, note: 'Fictional portfolio demo. Not a production record or digital signature.', createdAt: new Date().toISOString(), records: structuredClone(records), history: structuredClone(events) };
    downloadURL = URL.createObjectURL(new Blob([JSON.stringify(snapshot, null, 2)], {type:'application/json'}));
    document.querySelector('#download-snapshot').href = downloadURL;
    document.querySelector('#snapshot').hidden = false; render(); document.querySelector('#snapshot').focus();
  });
  document.querySelector('#reset-demo').addEventListener('click', reset);
  reset();
})();
