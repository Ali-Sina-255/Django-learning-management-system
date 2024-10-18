/**
 * @license Copyright (c) 2003-2024, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see LICENSE.md or https://ckeditor.com/legal/ckeditor-oss-license
 */
/**
 * @module ui/highlightedtext/buttonlabelwithhighlightview
 */
import type ButtonLabel from '../button/buttonlabel.js';
import HighlightedTextView from './highlightedtextview.js';
/**
 * A button label view that can highlight a text fragment.
 */
export default class ButtonLabelWithHighlightView extends HighlightedTextView implements ButtonLabel {
    /**
     * @inheritDoc
     */
    style: string | undefined;
    /**
     * @inheritDoc
     */
    text: string | undefined;
    /**
     * @inheritDoc
     */
    id: string | undefined;
    /**
     * @inheritDoc
     */
    constructor();
}
