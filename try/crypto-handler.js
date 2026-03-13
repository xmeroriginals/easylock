const MAGIC_HEADER = new Uint8Array([69, 76, 67, 75]);
const VERSION = new Uint8Array([2, 0]);
const SALT_SIZE = 16;
const NONCE_SIZE = 16;
const CHUNK_SIZE = 64 * 1024;
const HMAC_SIZE = 32;
const ARGON2_TIME_COST = 2;
const ARGON2_MEMORY_COST = 102400;
const ARGON2_PARALLELISM = 4;
let selectedFiles = [];
let currentMode = null;
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const actionArea = document.getElementById('actionArea');
const modalTitle = document.getElementById('modalTitle');
const statusMsg = document.getElementById('statusMsg');
const passwordModal = document.getElementById('passwordModal');
const passwordInput = document.getElementById('passwordInput');
const confirmBtn = document.getElementById('confirmBtn');
const cancelBtn = document.getElementById('cancelBtn');
const progressContainer = document.getElementById('progressContainer');
const progressBar = document.getElementById('progressBar');
const warningModal = document.getElementById('warningModal');
const continueBtn = document.getElementById('continueBtn');

dropZone.onclick = () => fileInput.click();
fileInput.onchange = (e) => handleFiles(e.target.files);

dropZone.ondragover = (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
};

dropZone.ondragleave = () => dropZone.classList.remove('drag-over');

dropZone.ondrop = (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    handleFiles(e.dataTransfer.files);
};

function handleFiles(files) {
    let largeFileFound = false;
    for (let file of files) {
        if (file.size > 512 * 1024 * 1024) {
            largeFileFound = true;
        }
        if (!selectedFiles.find(f => f.name === file.name && f.size === file.size)) {
            selectedFiles.push(file);
        }
    }

    if (largeFileFound) {
        warningModal.style.display = 'flex';
    } else {
        updateFileList();
    }
}

continueBtn.onclick = () => {
    warningModal.style.display = 'none';
    updateFileList();
};

function updateFileList() {
    fileList.innerHTML = '';
    selectedFiles.forEach((file, index) => {
        const item = document.createElement('div');
        item.className = 'file-item';

        const fileInfo = document.createElement('div');
        fileInfo.className = 'file-info';

        const icon = document.createElement('i');
        icon.className = 'material-icons';
        icon.textContent = file.name.endsWith('.elock') ? 'lock' : 'insert_drive_file';

        const details = document.createElement('div');
        const nameDiv = document.createElement('div');
        nameDiv.className = 'file-name';
        nameDiv.textContent = file.name;

        const sizeDiv = document.createElement('div');
        sizeDiv.className = 'file-size';
        sizeDiv.textContent = `${(file.size / 1024).toFixed(2)} KB`;

        details.appendChild(nameDiv);
        details.appendChild(sizeDiv);
        fileInfo.appendChild(icon);
        fileInfo.appendChild(details);

        const removeIcon = document.createElement('i');
        removeIcon.className = 'material-icons remove-file';
        removeIcon.textContent = 'close';
        removeIcon.onclick = () => removeFile(index);

        item.appendChild(fileInfo);
        item.appendChild(removeIcon);
        fileList.appendChild(item);
    });
    actionArea.style.display = selectedFiles.length > 0 ? 'flex' : 'none';
}

window.removeFile = (index) => {
    selectedFiles.splice(index, 1);
    updateFileList();
};

document.getElementById('encryptBtn').onclick = () => showPasswordModal('encrypt');
document.getElementById('decryptBtn').onclick = () => showPasswordModal('decrypt');

function showPasswordModal(mode) {
    currentMode = mode;
    const lang = navigator.language.startsWith('tr') ? 'TR' : 'EN';
    const titleKey = mode === 'encrypt' ? 'pwd_title_encrypt' : 'pwd_title_decrypt';
    const titles = {
        'EN': { 'encrypt': 'Encrypt Files', 'decrypt': 'Decrypt Files' },
        'TR': { 'encrypt': 'Dosyaları Şifrele', 'decrypt': 'Şifreyi Çöz' }
    };

    modalTitle.textContent = titles[lang][mode];
    passwordInput.value = '';
    passwordModal.style.display = 'flex';
    passwordInput.focus();
}

cancelBtn.onclick = () => {
    passwordModal.style.display = 'none';
};

confirmBtn.onclick = async () => {
    const passwordStr = passwordInput.value;
    if (passwordStr.length < 12) {
        alert('Security Alert: Password must be at least 12 characters for strong protection.');
        return;
    }

    const encoder = new TextEncoder();
    const passwordBytes = encoder.encode(passwordStr);
    passwordInput.value = '';
    passwordModal.style.display = 'none';
    await processFiles(passwordBytes);

    zeroOut(passwordBytes);
};

async function processFiles(passwordBytes) {
    statusMsg.className = 'status-message info';
    progressContainer.style.display = 'block';

    for (let i = 0; i < selectedFiles.length; i++) {
        const file = selectedFiles[i];
        try {
            statusMsg.textContent = `Processing ${file.name}...`;
            updateProgress(0);

            if (currentMode === 'encrypt') {
                await encryptFile(file, passwordBytes);
            } else {
                await decryptFile(file, passwordBytes);
            }

            statusMsg.className = 'status-message success';
            statusMsg.textContent = 'Success! Your files are ready.';
        } catch (err) {
            console.error(err);
            statusMsg.className = 'status-message error';
            statusMsg.textContent = `Error processing ${file.name}: ${err.message}`;
            break;
        }
    }

    setTimeout(() => {
        progressContainer.style.display = 'none';
        updateFileList();
    }, 2000);
}

function updateProgress(percent) {
    progressBar.style.width = percent + '%';
}

function zeroOut(arr) {
    if (arr) arr.fill(0);
}

async function deriveKeys(passwordBytes, salt, t, m, p) {
    const result = await argon2.hash({
        pass: passwordBytes,
        salt: salt,
        time: t,
        mem: m,
        parallelism: p,
        type: argon2.ArgonType.Argon2id,
        hashLen: 64
    });

    const encKey = result.hash.slice(0, 32);
    const macKey = result.hash.slice(32, 64);
    return { encKey, macKey };
}

function getCounterForChunk(initialNonce, chunkIndex) {
    const counter = new Uint8Array(initialNonce);
    const blocksPerChunk = CHUNK_SIZE / 16;
    let increment = chunkIndex * blocksPerChunk;

    for (let i = counter.length - 1; i >= 0 && increment > 0; i--) {
        const sum = counter[i] + (increment & 0xff);
        counter[i] = sum & 0xff;
        increment = (increment >> 8) + (sum >> 8);
    }
    return counter;
}

async function encryptFile(file, passwordBytes) {
    const salt = window.crypto.getRandomValues(new Uint8Array(SALT_SIZE));
    const nonce = window.crypto.getRandomValues(new Uint8Array(NONCE_SIZE));

    const { encKey, macKey } = await deriveKeys(passwordBytes, salt, ARGON2_TIME_COST, ARGON2_MEMORY_COST, ARGON2_PARALLELISM);

    const aesKeyObj = await crypto.subtle.importKey(
        'raw', encKey, { name: 'AES-CTR' }, false, ['encrypt']
    );

    const hmacHasher = sha256.hmac.create(macKey);
    const params = new Uint8Array(12);
    const paramsView = new DataView(params.buffer);
    paramsView.setUint32(0, ARGON2_TIME_COST, true);
    paramsView.setUint32(4, ARGON2_MEMORY_COST, true);
    paramsView.setUint32(8, ARGON2_PARALLELISM, true);
    const header = new Uint8Array(MAGIC_HEADER.length + VERSION.length + params.length + SALT_SIZE + NONCE_SIZE);
    header.set(MAGIC_HEADER, 0);
    header.set(VERSION, MAGIC_HEADER.length);
    header.set(params, MAGIC_HEADER.length + VERSION.length);
    header.set(salt, MAGIC_HEADER.length + VERSION.length + params.length);
    header.set(nonce, MAGIC_HEADER.length + VERSION.length + params.length + SALT_SIZE);
    hmacHasher.update(header);
    const encryptedChunks = [];
    const totalChunks = Math.ceil(file.size / CHUNK_SIZE);

    for (let i = 0; i < totalChunks; i++) {
        const start = i * CHUNK_SIZE;
        const end = Math.min(start + CHUNK_SIZE, file.size);
        const chunkBuffer = await file.slice(start, end).arrayBuffer();

        const chunkCounter = getCounterForChunk(nonce, i);
        const encryptedChunk = await crypto.subtle.encrypt(
            { name: 'AES-CTR', counter: chunkCounter, length: 128 },
            aesKeyObj,
            chunkBuffer
        );

        const encryptedBytes = new Uint8Array(encryptedChunk);
        hmacHasher.update(encryptedBytes);
        encryptedChunks.push(encryptedBytes);
        updateProgress(Math.round(((i + 1) / totalChunks) * 100));
    }

    const tag = hmacHasher.array();
    const finalBlob = new Blob([header, ...encryptedChunks, new Uint8Array(tag)]);
    saveFile(finalBlob, file.name + '.elock');
    zeroOut(encKey);
    zeroOut(macKey);
}

async function decryptFile(file, passwordBytes) {
    const maxHeaderSize = MAGIC_HEADER.length + VERSION.length + 12 + SALT_SIZE + NONCE_SIZE;
    const headerBuffer = await file.slice(0, maxHeaderSize).arrayBuffer();
    const header = new Uint8Array(headerBuffer);

    let offset = 0;
    const magic = header.slice(offset, offset += 4);
    if (!compareUint8(magic, MAGIC_HEADER)) throw new Error('Not an EasyLock file or unknown format.');

    const version = header.slice(offset, offset += 2);
    let t, m, p;
    let currentHeaderSize;

    if (compareUint8(version, new Uint8Array([2, 0]))) {
        const paramsBytes = header.slice(offset, offset += 12);
        const view = new DataView(paramsBytes.buffer, paramsBytes.byteOffset, paramsBytes.byteLength);
        t = view.getUint32(0, true);
        m = view.getUint32(4, true);
        p = view.getUint32(8, true);
        currentHeaderSize = MAGIC_HEADER.length + VERSION.length + 12 + SALT_SIZE + NONCE_SIZE;
    } else if (compareUint8(version, new Uint8Array([1, 0]))) {
        t = 2; m = 102400; p = 4;
        currentHeaderSize = MAGIC_HEADER.length + VERSION.length + SALT_SIZE + NONCE_SIZE;
    } else {
        throw new Error('Unsupported version.');
    }

    const salt = header.slice(offset, offset += SALT_SIZE);
    const nonce = header.slice(offset, offset += NONCE_SIZE);
    const { encKey, macKey } = await deriveKeys(passwordBytes, salt, t, m, p);
    const hmacHasher = sha256.hmac.create(macKey);
    hmacHasher.update(header.slice(0, currentHeaderSize));
    const ciphertextEnd = file.size - HMAC_SIZE;
    const ciphertextChunks = [];
    const totalCiphertextBytes = ciphertextEnd - currentHeaderSize;
    const totalChunks = Math.ceil(totalCiphertextBytes / CHUNK_SIZE);

    for (let i = 0; i < totalChunks; i++) {
        const start = currentHeaderSize + (i * CHUNK_SIZE);
        const end = Math.min(start + CHUNK_SIZE, ciphertextEnd);
        const chunkBuffer = await file.slice(start, end).arrayBuffer();
        const chunkBytes = new Uint8Array(chunkBuffer);

        hmacHasher.update(chunkBytes);
        ciphertextChunks.push(chunkBytes);
        updateProgress(Math.round(((i + 1) / totalChunks) * 50));
    }

    const calculatedTag = hmacHasher.array();
    const storedTagBuffer = await file.slice(ciphertextEnd).arrayBuffer();
    const storedTag = new Uint8Array(storedTagBuffer);

    if (!compareUint8(new Uint8Array(calculatedTag), storedTag)) {
        zeroOut(encKey);
        zeroOut(macKey);
        throw new Error('Invalid password or corrupted file.');
    }

    const aesKeyObj = await crypto.subtle.importKey(
        'raw', encKey, { name: 'AES-CTR' }, false, ['decrypt']
    );

    const decryptedChunks = [];
    for (let i = 0; i < ciphertextChunks.length; i++) {
        const chunkBytes = ciphertextChunks[i];
        const chunkCounter = getCounterForChunk(nonce, i);

        const decryptedChunk = await crypto.subtle.decrypt(
            { name: 'AES-CTR', counter: chunkCounter, length: 128 },
            aesKeyObj,
            chunkBytes.buffer
        );

        decryptedChunks.push(new Uint8Array(decryptedChunk));
        updateProgress(50 + Math.round(((i + 1) / ciphertextChunks.length) * 50));
    }

    const outName = file.name.endsWith('.elock') ? file.name.slice(0, -6) : file.name + '.decrypted';
    saveFile(new Blob(decryptedChunks), outName);

    zeroOut(encKey);
    zeroOut(macKey);
}

function compareUint8(a, b) {
    if (a.length !== b.length) return false;
    let diff = 0;
    for (let i = 0; i < a.length; i++) {
        diff |= a[i] ^ b[i];
    }
    return diff === 0;
}

function saveFile(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}
