/** @odoo-module **/

/**
 * Migration notes (v15 ➜ v18, option "legacy/jQuery"):
 * - On reste en publicWidget (legacy) mais en module ES avec le header @odoo-module.
 * - Imports modernes pour _t + renderToElement.
 * - On conserve le widget NameAndSignature (module legacy). Si le chemin change
 *   dans ta base, adapte l'import indiqué plus bas (TODO).
 */

import publicWidget from "@web/legacy/js/public/public_widget";
import { _t } from "@web/core/l10n/translation";
import { renderToElement } from "@web/core/utils/render";

// ⚠️ Legacy import: dans la plupart des installations v17/v18, ce module legacy existe encore.
// Si ta base ne le trouve pas, essaie l’un de ces chemins (et supprime le require ci-dessous):
//   - import { NameAndSignature } from "@web/views/fields/signature/name_and_signature"; (selon édition)
//   - import { NameAndSignature } from "@web/legacy/js/core/name_and_signature";
// Pour rester 100% compatible avec la v15 d’origine, on garde require ici :
const { NameAndSignature } = require("web.name_and_signature"); // eslint-disable-line

publicWidget.registry.SignatureFormBRConsult = publicWidget.Widget.extend({
    /**
     * Ce widget s’instancie sur le template de signature du portail.
     * Ajuste le sélecteur si besoin (par ex. ".o_portal_sign").
     */
    selector: ".o_portal_signature_wrapper",

    template: "portal.portal_signature",
    xmlDependencies: ["/portal/static/src/xml/portal_signature.xml"],

    events: {
        "click .o_portal_sign_submit": "_onClickSignSubmit",
    },
    custom_events: {
        signature_changed: "_onChangeSignature",
    },

    /**
     * Constructor
     *
     * @param {Widget} parent
     * @param {Object} options
     *   - callUrl {string} : route RPC serveur
     *   - sendLabel {string}: libellé du bouton
     *   - rpcParams {Object}: params additionnels RPC
     *   - nameAndSignatureOptions {Object}: options du widget signature
     */
    init() {
        this._super(...arguments);

        this.csrf_token = window.odoo && window.odoo.csrf_token;
        const options = this.options || {};

        this.callUrl = options.callUrl || "";
        this.rpcParams = options.rpcParams || {};
        this.sendLabel = options.sendLabel || _t("Accept & Sign");

        this.nameAndSignature = new NameAndSignature(
            this,
            options.nameAndSignatureOptions || {}
        );
    },

    /**
     * Récupération des éléments DOM et insertion du sous-widget signature.
     */
    async start() {
        this.$confirm_btn = this.$(".o_portal_sign_submit");
        this.$controls = this.$(".o_portal_sign_controls");
        await Promise.all([
            this.nameAndSignature.replace(this.$(".o_web_sign_name_and_signature")),
            this._super(...arguments),
        ]);
        this.nameAndSignature.resetSignature();
    },

    // --------------------------
    // Public helpers (compat)
    // --------------------------

    focusName() {
        this.nameAndSignature.focusName();
    },

    resetSignature() {
        return this.nameAndSignature.resetSignature();
    },

    // --------------------------
    // Handlers
    // --------------------------

    async _onClickSignSubmit(ev) {
        ev.preventDefault();

        if (!this.nameAndSignature.validateSignature()) {
            return;
        }

        const name = this.nameAndSignature.getName();
        const signature = this.nameAndSignature.getSignatureImage()[1];
        const comment_mentor =
            this.nameAndSignature.getCommentMentor &&
            this.nameAndSignature.getCommentMentor();

        const payload = {
            ...this.rpcParams,
            name,
            signature,
            comment_mentor,
        };

        try {
            // publicWidget fournit this._rpc (compat JSON-RPC).
            const data = await this._rpc({
                route: this.callUrl,
                params: payload,
            });

            if (data?.error) {
                this.$(".o_portal_sign_error_msg").remove();
                const errorEl = renderToElement("portal.portal_signature_error", {
                    widget: data,
                });
                this.$controls.prepend(errorEl);
            } else if (data?.success) {
                const successEl = renderToElement("portal.portal_signature_success", {
                    widget: data,
                });
                this.$el.empty().append(successEl);
            }

            if (data?.force_refresh) {
                if (data.redirect_url) {
                    window.location = data.redirect_url;
                } else {
                    window.location.reload();
                }
            }
        } catch (e) {
            // fallback propre
            console.error("Signature RPC failed:", e);
            const msg = renderToElement("portal.portal_signature_error", {
                widget: { error: true, message: _t("Unexpected error. Please try again.") },
            });
            this.$controls.prepend(msg);
        }
    },

    _onChangeSignature() {
        const isEmpty = this.nameAndSignature.isSignatureEmpty();
        this.$confirm_btn.prop("disabled", isEmpty);
    },
});

export default publicWidget.registry.SignatureFormBRConsult;
