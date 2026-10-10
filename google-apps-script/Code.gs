const RECIPIENT_EMAIL = "zbatayoub09@gmail.com";

function doPost(e) {
  const p = (e && e.parameter) ? e.parameter : {};
  const name = clean_(p["Nom"]);
  const phone = clean_(p["Téléphone"]);
  const email = clean_(p["E-mail du client"]);
  const city = clean_(p["Ville"]);
  const product = clean_(p["Produit demandé"]);
  const page = clean_(p["Page du produit"]);
  const message = clean_(p["Message"]);

  if (!name || !phone || !message) {
    return page_("Informations manquantes", "Merci de revenir au formulaire et de remplir le nom, le téléphone et le message.");
  }

  const subject = "Nouvelle demande CNC Forge Maroc — " + (product || "Demande de devis");
  const body = [
    "Nouvelle demande reçue depuis le site CNC Forge Maroc",
    "",
    "Nom : " + name,
    "Téléphone / WhatsApp : " + phone,
    "E-mail : " + (email || "Non renseigné"),
    "Ville : " + (city || "Non renseignée"),
    "Produit demandé : " + (product || "Non précisé"),
    "Page : " + (page || "Non renseignée"),
    "",
    "Message :",
    message
  ].join("\n");

  MailApp.sendEmail({
    to: RECIPIENT_EMAIL,
    subject: subject,
    body: body,
    replyTo: validEmail_(email) ? email : undefined,
    name: "CNC Forge Maroc — Formulaire"
  });

  return page_("Demande envoyée", "Merci " + escapeHtml_(name) + " ! Votre demande a été envoyée. Vous pouvez fermer cet onglet.");
}

function clean_(value) {
  return String(value || "").replace(/[\\r\\n\\t]+/g, " ").trim().slice(0, 3000);
}

function validEmail_(value) {
  return /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(String(value || ""));
}

function escapeHtml_(value) {
  return String(value).replace(/[&<>"']/g, function (c) {
    return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c];
  });
}

function page_(title, message) {
  return HtmlService.createHtmlOutput(
    '<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' +
    '<title>' + escapeHtml_(title) + '</title>' +
    '<body style="font-family:Arial,sans-serif;background:#f5f7fb;color:#111827;padding:32px;line-height:1.6">' +
    '<main style="max-width:560px;margin:8vh auto;background:white;padding:28px;border-radius:18px;box-shadow:0 10px 35px #10182712">' +
    '<h1 style="font-size:24px">' + escapeHtml_(title) + '</h1><p>' + message + '</p>' +
    '<p style="color:#687386;font-size:13px">CNC Forge Maroc</p></main></body></html>'
  );
}
