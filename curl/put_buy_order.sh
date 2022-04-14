curl \
    --header "content-type: application/json" \
    --request PUT \
    --data '{"currency":"USD","amount":"123.45","idempotence_key":"5fa733ae-82b4-4ac0-8478-35ff30dae879"}' \
    http://localhost:8777/buy_order