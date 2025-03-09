const domainInput = document.getElementById('domain-input');
const checkButton = document.getElementById('check-button');
const resultSection = document.getElementById('result');

checkButton.addEventListener('click', async () => {
    const domain = domainInput.value.trim();
    const domainPattern = /^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$/;

    if (!domainPattern.test(domain)) {
        resultSection.innerHTML = '请输入有效的域名。';
        return;
    }

    try {
        const response = await fetch('/check-domain', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ domain }),
        });

        if (!response.ok) {
            throw new Error('网络错误');
        }

        const data = await response.json();
        if (data.available) {
            resultSection.innerHTML = `域名 ${domain} 未注册。`;
        } else {
            resultSection.innerHTML = `域名 ${domain} 已注册。注册时间: ${data.registrationDate}<br>WHOIS信息: ${data.whoisInfo}`;
        }
    } catch (error) {
        resultSection.innerHTML = '查询失败，请稍后再试。';
    }
});

document.getElementById('domain-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const domain = document.getElementById('domain-input').value;
    const resultDiv = document.getElementById('result');

    fetch('/api/check_domain', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ domain: domain })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            resultDiv.textContent = `Error: ${data.error}`;
        } else if (data.registered) {
            resultDiv.textContent = `Domain is registered. Registration date: ${data.registration_date}`;
        } else {
            resultDiv.textContent = 'Domain is not registered.';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        resultDiv.textContent = '查询失败，请稍后再试。';
    });
});